"""
app.py
Smart Recipe Assistant — main Streamlit application.

Run with:  streamlit run app.py
"""

import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv  # Added to load environment variables

import gemini_client
from i18n import SUPPORTED_LANGUAGES, get_ui_strings, UI_STRINGS
from styles import CUSTOM_CSS
from pdf_export import build_shopping_list_pdf, build_recipe_pdf

# Load any variables declared in the .env file
load_dotenv()

st.set_page_config(
    page_title="Smart Recipe Assistant",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Session state initialization
# ----------------------------------------------------------------------
def init_state():
    defaults = {
        "ingredients": [],
        "recipes": [],
        "selected_recipe": None,
        "recipe_details_cache": {},
        "favorites": {},
        "lang_code": "en",
        "translated_ui_cache": {},
        "api_key": os.getenv("GEMINI_API_KEY", ""),  # Automatically retrieve from .env if present
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_state()


def T() -> dict:
    """Return the active UI string dictionary, auto-translating & caching
    on first use if the chosen language isn't hand-written in i18n.py."""
    lang = st.session_state.lang_code
    if lang in UI_STRINGS:
        return get_ui_strings(lang)
    if lang in st.session_state.translated_ui_cache:
        return st.session_state.translated_ui_cache[lang]
    if st.session_state.get("api_key"):
        try:
            gemini_client.configure(st.session_state.api_key)
            translated = gemini_client.translate_ui_strings(UI_STRINGS["en"], lang)
            st.session_state.translated_ui_cache[lang] = translated
            return translated
        except Exception:
            pass
    return get_ui_strings("en")


# ----------------------------------------------------------------------
# Sidebar — settings
# ----------------------------------------------------------------------
with st.sidebar:
    lang_names = list(SUPPORTED_LANGUAGES.keys())
    chosen_name = st.selectbox("🌐 Language / भाषा / Idioma", lang_names, index=0)
    st.session_state.lang_code = SUPPORTED_LANGUAGES[chosen_name]

    strings = T()
    st.header(strings["sidebar_settings"])

    # Pre-fill with .env key if available
    api_key_input = st.text_input(
        strings["api_key_label"], 
        value=st.session_state.get("api_key", ""),
        type="password", 
        help=strings["api_key_help"]
    )
    if api_key_input:
        st.session_state.api_key = api_key_input

    st.divider()
    diet_pref = st.selectbox(
        strings["diet_pref"],
        ["None", "Vegetarian", "Vegan", "Keto", "Low-Carb", "Gluten-Free", "High-Protein"],
    )
    cuisine_pref = st.selectbox(
        strings["cuisine_pref"],
        ["Any", "Indian", "Italian", "Mexican", "Chinese", "Thai", "Mediterranean", "American", "Japanese"],
    )
    servings = st.slider(strings["servings"], 1, 10, 2)
    allergies = st.text_input(strings["allergy_label"], placeholder="e.g. peanuts, shellfish")

strings = T()  # refresh after possible translation triggered by api key

# ----------------------------------------------------------------------
# Hero header
# ----------------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero-banner">
        <p class="hero-title">{strings['app_title']}</p>
        <p class="hero-subtitle">{strings['app_subtitle']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_ingredients, tab_recipes, tab_details, tab_favorites = st.tabs(
    [strings["tab_ingredients"], strings["tab_recipes"], strings["tab_details"], strings["tab_favorites"]]
)

# ----------------------------------------------------------------------
# TAB 1: Ingredients
# ----------------------------------------------------------------------
with tab_ingredients:
    st.markdown(f'<div class="section-header">{strings["ingredient_input_header"]}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        text_input = st.text_area(strings["ingredient_text_label"], placeholder="tomato, onion, rice, eggs...")
        if text_input:
            typed = [i.strip() for i in text_input.split(",") if i.strip()]
        else:
            typed = []

    with col2:
        uploaded_image = st.file_uploader(
            strings["ingredient_upload_label"], type=["png", "jpg", "jpeg", "webp"]
        )
        detected = []
        if uploaded_image is not None:
            img = Image.open(uploaded_image)
            st.image(img, use_container_width=True)
            if st.button(strings["detect_button"]):
                if not st.session_state.get("api_key"):
                    st.warning(strings["no_api_key_warning"])
                else:
                    with st.spinner(strings["generating_recipes"]):
                        try:
                            gemini_client.configure(st.session_state.api_key)
                            detected = gemini_client.detect_ingredients_from_image(
                                img, st.session_state.lang_code
                            )
                            st.session_state.ingredients = list(
                                set(st.session_state.ingredients + detected)
                            )
                        except Exception as e:
                            st.error(f"{e}")

    # merge typed ingredients into master list
    if typed:
        st.session_state.ingredients = list(set(st.session_state.ingredients + typed))

    if st.session_state.ingredients:
        st.markdown(f"**{strings['detected_ingredients']}:**")
        chips_html = "".join(
            f'<span class="ingredient-chip">{ing}</span>' for ing in st.session_state.ingredients
        )
        st.markdown(chips_html, unsafe_allow_html=True)

        if st.button("🗑️ " + ("Clear all" if st.session_state.lang_code == "en" else "Clear")):
            st.session_state.ingredients = []
            st.rerun()

    st.write("")
    if st.button(strings["find_recipes_button"], type="primary"):
        if not st.session_state.ingredients:
            st.warning(strings["no_ingredients_warning"])
        elif not st.session_state.get("api_key"):
            st.warning(strings["no_api_key_warning"])
        else:
            with st.spinner(strings["generating_recipes"]):
                try:
                    gemini_client.configure(st.session_state.api_key)
                    recipes = gemini_client.recommend_recipes(
                        st.session_state.ingredients,
                        language=st.session_state.lang_code,
                        diet_pref=diet_pref,
                        cuisine_pref=cuisine_pref,
                        allergies=allergies,
                        servings=servings,
                    )
                    st.session_state.recipes = recipes
                    st.session_state.recipe_details_cache = {}
                    st.success("✅")
                except Exception as e:
                    st.error(f"{e}")

# ----------------------------------------------------------------------
# TAB 2: Recipes list
# ----------------------------------------------------------------------
with tab_recipes:
    if not st.session_state.recipes:
        st.info(strings["select_recipe_prompt"] if False else strings["no_ingredients_warning"])
    else:
        diff_class_map = {
            "Easy": "badge-diff-easy",
            "Medium": "badge-diff-medium",
            "Hard": "badge-diff-hard",
        }
        cols = st.columns(2)
        for idx, recipe in enumerate(st.session_state.recipes):
            with cols[idx % 2]:
                match_pct = recipe.get("match_percent", 0)
                diff = recipe.get("difficulty", "Medium")
                diff_class = diff_class_map.get(diff, "badge-diff-medium")
                st.markdown(
                    f"""
                    <div class="recipe-card">
                        <div class="recipe-title">{recipe.get('title','')}</div>
                        <div style="color:#777; font-size:0.9rem;">{recipe.get('short_description','')}</div>
                        <div class="recipe-meta">
                            <span class="badge badge-cuisine">{recipe.get('cuisine','')}</span>
                            <span class="badge badge-time">⏱ {recipe.get('prep_time_minutes','?')} min</span>
                            <span class="badge {diff_class}">{diff}</span>
                            <span class="badge badge-match">{strings['match_score']}: {match_pct}%</span>
                        </div>
                        <div class="match-bar-bg"><div class="match-bar-fill" style="width:{match_pct}%;"></div></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                bcol1, bcol2 = st.columns([2, 1])
                with bcol1:
                    if st.button(strings["view_details"], key=f"view_{recipe.get('id', idx)}"):
                        st.session_state.selected_recipe = recipe
                        st.rerun()
                with bcol2:
                    rid = recipe.get("id", str(idx))
                    is_fav = rid in st.session_state.favorites
                    fav_label = "💔" if is_fav else "🤍"
                    if st.button(fav_label, key=f"fav_{rid}"):
                        if is_fav:
                            del st.session_state.favorites[rid]
                            st.toast(strings["removed_favorite"])
                        else:
                            st.session_state.favorites[rid] = recipe
                            st.toast(strings["added_favorite"])
                        st.rerun()

# ----------------------------------------------------------------------
# TAB 3: Full recipe details, nutrition, shopping list, healthier alts
# ----------------------------------------------------------------------
with tab_details:
    recipe = st.session_state.selected_recipe
    if not recipe:
        st.info(strings["select_recipe_prompt"])
    else:
        cache_key = recipe.get("id", recipe.get("title"))
        if cache_key not in st.session_state.recipe_details_cache:
            if not st.session_state.get("api_key"):
                st.warning(strings["no_api_key_warning"])
                detail = None
            else:
                with st.spinner(strings["generating_details"]):
                    try:
                        gemini_client.configure(st.session_state.api_key)
                        detail = gemini_client.get_recipe_full_details(
                            recipe_title=recipe.get("title", ""),
                            matched_ingredients=recipe.get("matched_ingredients", []),
                            missing_ingredients=recipe.get("missing_ingredients", []),
                            language=st.session_state.lang_code,
                            servings=servings,
                            diet_pref=diet_pref,
                        )
                        st.session_state.recipe_details_cache[cache_key] = detail
                    except Exception as e:
                        st.error(f"{e}")
                        detail = None
        else:
            detail = st.session_state.recipe_details_cache[cache_key]

        if detail:
            st.markdown(f"## {detail.get('title','')}")
            m1, m2, m3 = st.columns(3)
            m1.markdown(
                f'<span class="badge badge-time">⏱ {strings["prep_time"]}: {detail.get("prep_time_minutes","?")} min</span>',
                unsafe_allow_html=True,
            )
            m2.markdown(
                f'<span class="badge badge-diff-medium">{strings["difficulty"]}: {detail.get("difficulty","")}</span>',
                unsafe_allow_html=True,
            )
            m3.markdown(
                f'<span class="badge badge-cuisine">{strings["servings_label"]}: {detail.get("servings","")}</span>',
                unsafe_allow_html=True,
            )

            st.markdown(f'<div class="section-header">{strings["ingredients_needed"]}</div>', unsafe_allow_html=True)
            for ing in detail.get("full_ingredient_list", []):
                mark = "✅" if ing.get("have_it") else "🛒"
                st.markdown(f"- {mark} **{ing.get('name','')}** — {ing.get('quantity','')}")

            st.markdown(f'<div class="section-header">{strings["instructions"]}</div>', unsafe_allow_html=True)
            for i, step in enumerate(detail.get("instructions", []), start=1):
                st.markdown(f"**{i}.** {step}")

            nutrition = detail.get("nutrition", {})
            if nutrition:
                st.markdown(f'<div class="section-header">{strings["nutrition_header"]}</div>', unsafe_allow_html=True)
                n1, n2, n3, n4, n5 = st.columns(5)
                tiles = [
                    (n1, strings["calories"], nutrition.get("calories_kcal", "-"), "kcal"),
                    (n2, strings["protein"], nutrition.get("protein_g", "-"), "g"),
                    (n3, strings["carbs"], nutrition.get("carbs_g", "-"), "g"),
                    (n4, strings["fat"], nutrition.get("fat_g", "-"), "g"),
                    (n5, strings["fiber"], nutrition.get("fiber_g", "-"), "g"),
                ]
                for col, label, value, unit in tiles:
                    col.markdown(
                        f"""
                        <div class="nutrition-tile">
                            <div class="nutrition-value">{value}<span style="font-size:0.9rem;">{unit}</span></div>
                            <div class="nutrition-label">{label}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            shopping_list = detail.get("shopping_list", [])
            if shopping_list:
                st.markdown(f'<div class="section-header">{strings["shopping_list_header"]}</div>', unsafe_allow_html=True)
                st.caption(strings["shopping_list_caption"])
                for item in shopping_list:
                    st.markdown(
                        f"""<div class="shop-item">🛒 <b>{item.get('item','')}</b>
                        — {item.get('quantity','')}
                        <span style="color:#999;">({item.get('category','')})</span></div>""",
                        unsafe_allow_html=True,
                    )
                pdf_bytes = build_shopping_list_pdf(detail.get("title", ""), shopping_list, strings)
                st.download_button(
                    strings["download_shopping_list"],
                    data=pdf_bytes,
                    file_name="shopping_list.pdf",
                    mime="application/pdf",
                )

            alternatives = detail.get("healthier_alternatives", [])
            if alternatives:
                st.markdown(f'<div class="section-header">{strings["healthier_header"]}</div>', unsafe_allow_html=True)
                for alt in alternatives:
                    st.markdown(
                        f"""<div class="healthy-tip">💡 <b>{alt.get('swap','')}</b><br>
                        <span style="color:#2e7d32;">{alt.get('benefit','')}</span></div>""",
                        unsafe_allow_html=True,
                    )

            if detail.get("chef_tip"):
                st.info(f"👨‍🍳 {detail['chef_tip']}")

            recipe_pdf_bytes = build_recipe_pdf(detail, strings)
            st.download_button(
                strings["download_recipe"],
                data=recipe_pdf_bytes,
                file_name="recipe.pdf",
                mime="application/pdf",
            )

# ----------------------------------------------------------------------
# TAB 4: Favorites
# ----------------------------------------------------------------------
with tab_favorites:
    if not st.session_state.favorites:
        st.info(strings["no_favorites"])
    else:
        cols = st.columns(2)
        for idx, (rid, recipe) in enumerate(st.session_state.favorites.items()):
            with cols[idx % 2]:
                st.markdown(
                    f"""
                    <div class="recipe-card">
                        <div class="recipe-title">⭐ {recipe.get('title','')}</div>
                        <div style="color:#777; font-size:0.9rem;">{recipe.get('short_description','')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(strings["view_details"], key=f"favview_{rid}"):
                    st.session_state.selected_recipe = recipe
                    st.rerun()

st.markdown(
    f'<p style="text-align:center; color:#aaa; font-size:0.8rem; margin-top:2rem;">{strings["footer_note"]}</p>',
    unsafe_allow_html=True,
)
{
  "servers": {
    "n8n": {
      "type": "http",
      "url": "https://jackdaniels.app.n8n.cloud/mcp-server/http"
    }
  }
}