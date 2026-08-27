"""
gemini_client.py
All calls to the Gemini API live here, kept separate from the Streamlit
UI code. Every generation function accepts a `language` argument and
instructs Gemini to respond in that language AND to return strict JSON,
which we parse into Python objects for the UI to render.
"""

import json
import re
import google.generativeai as genai
from PIL import Image

# UPGRADED: Updated from the deprecated gemini-2.0-flash to the current active model
TEXT_MODEL_NAME = "gemini-3.5-flash"
VISION_MODEL_NAME = "gemini-3.5-flash"


def configure(api_key: str):
    genai.configure(api_key=api_key)


def _get_model(name: str = TEXT_MODEL_NAME):
    return genai.GenerativeModel(name)


def _extract_json(raw_text: str):
    """Gemini sometimes wraps JSON in markdown fences or adds stray text.
    This strips fences and grabs the first {...} or [...] block."""
    cleaned = re.sub(r"```json|```", "", raw_text).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise


# ---------------------------------------------------------------------
# 1. Ingredient detection from an uploaded image
# ---------------------------------------------------------------------
def detect_ingredients_from_image(image: Image.Image, language: str = "en") -> list:
    model = _get_model(VISION_MODEL_NAME)
    prompt = f"""
You are a culinary vision expert. Look at this photo of a fridge, pantry,
or ingredients laid out on a counter. Identify every distinct food
ingredient visible.

Respond ONLY with a valid JSON array of ingredient names (strings, lowercase,
singular where natural), written in the language with code "{language}".
No explanation, no markdown, just the JSON array.
Example: ["tomato", "onion", "cheddar cheese"]
"""
    response = model.generate_content([prompt, image])
    return _extract_json(response.text)


# ---------------------------------------------------------------------
# 2. Recipe recommendations based on available ingredients
# ---------------------------------------------------------------------
def recommend_recipes(
    ingredients: list,
    language: str = "en",
    diet_pref: str = "None",
    cuisine_pref: str = "Any",
    allergies: str = "",
    servings: int = 2,
    num_recipes: int = 6,
) -> list:
    model = _get_model()
    prompt = f"""
You are an expert chef and nutritionist. The user has these ingredients
available at home: {", ".join(ingredients)}.

Preferences:
- Dietary preference: {diet_pref}
- Preferred cuisine: {cuisine_pref}
- Allergies / must avoid: {allergies if allergies else "none"}
- Servings needed: {servings}

Suggest {num_recipes} diverse recipes ranked by how well they match the
available ingredients (recipes needing few or no extra ingredients should
rank higher). Respect the dietary preference and NEVER include an allergen
listed above.

Respond ONLY with a valid JSON array, no markdown, no commentary. Each
element must have exactly this shape:
{{
  "id": "short-slug-id",
  "title": "Recipe name",
  "cuisine": "e.g. Italian",
  "match_percent": 0-100 integer (how many of the recipe's ingredients the
     user already has),
  "prep_time_minutes": integer,
  "difficulty": "Easy" | "Medium" | "Hard",
  "short_description": "one enticing sentence",
  "matched_ingredients": ["ingredient the user already has", ...],
  "missing_ingredients": ["ingredient the user needs to buy", ...]
}}

ALL text values (title, cuisine, description, ingredient names) must be
written in the language with code "{language}".
"""
    response = model.generate_content(prompt)
    return _extract_json(response.text)


# ---------------------------------------------------------------------
# 3. Full recipe detail: steps + nutrition + shopping list + healthier alts
#    (combined into one call for efficiency / consistency)
# ---------------------------------------------------------------------
def get_recipe_full_details(
    recipe_title: str,
    matched_ingredients: list,
    missing_ingredients: list,
    language: str = "en",
    servings: int = 2,
    diet_pref: str = "None",
) -> dict:
    model = _get_model()
    prompt = f"""
You are an expert chef and registered dietitian. Produce full details for
the recipe titled "{recipe_title}" for {servings} servings, respecting a
"{diet_pref}" dietary preference.

The user already has: {", ".join(matched_ingredients) if matched_ingredients else "nothing relevant"}.
The user still needs to buy: {", ".join(missing_ingredients) if missing_ingredients else "nothing extra"}.

Respond ONLY with valid JSON (no markdown fences, no commentary) in EXACTLY
this shape:
{{
  "title": "...",
  "servings": {servings},
  "prep_time_minutes": integer,
  "difficulty": "Easy" | "Medium" | "Hard",
  "full_ingredient_list": [
      {{"name": "...", "quantity": "e.g. 2 cups", "have_it": true}}
  ],
  "instructions": ["step 1", "step 2", "..."],
  "nutrition": {{
      "calories_kcal": number,
      "protein_g": number,
      "carbs_g": number,
      "fat_g": number,
      "fiber_g": number,
      "per_serving": true
  }},
  "shopping_list": [
      {{"item": "...", "quantity": "e.g. 500 g", "category": "e.g. Produce"}}
  ],
  "healthier_alternatives": [
      {{"swap": "e.g. Use Greek yogurt instead of sour cream",
        "benefit": "e.g. Cuts fat by 40% and adds protein"}}
  ],
  "chef_tip": "one short creative tip or flavor variation"
}}

ALL text (ingredient names, instructions, tips, categories) must be written
in the language with code "{language}". Numbers stay numeric (no units
inside number fields).
"""
    response = model.generate_content(prompt)
    return _extract_json(response.text)


# ---------------------------------------------------------------------
# 4. One-shot translation of the static UI string dictionary, used when
#    the user picks a language we haven't hand-translated in i18n.py
# ---------------------------------------------------------------------
def translate_ui_strings(base_strings: dict, target_language: str) -> dict:
    model = _get_model()
    prompt = f"""
Translate every VALUE (not the keys) in this JSON object into the language
with code "{target_language}". Keep emojis exactly where they already are.
Keep the exact same keys. Respond ONLY with the translated JSON object,
no markdown, no commentary.

{json.dumps(base_strings, ensure_ascii=False)}
"""
    response = model.generate_content(prompt)
    return _extract_json(response.text)