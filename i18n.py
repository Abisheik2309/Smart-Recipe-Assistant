"""
i18n.py
Handles UI translation (static strings) and the master list of languages
that can be used both for the interface and for Gemini-generated content
(recipes, nutrition, shopping lists, tips) so the ENTIRE app — not just
labels — appears in the user's chosen language.
"""

# Languages offered in the sidebar selector.
# Key = language name shown to user, Value = code passed to Gemini prompts
SUPPORTED_LANGUAGES = {
    "English": "en",
    "हिंदी (Hindi)": "hi",
    "தமிழ் (Tamil)": "ta",
    "తెలుగు (Telugu)": "te",
    "বাংলা (Bengali)": "bn",
    "मराठी (Marathi)": "mr",
    "Español (Spanish)": "es",
    "Français (French)": "fr",
    "Deutsch (German)": "de",
    "中文 (Chinese)": "zh",
    "日本語 (Japanese)": "ja",
    "العربية (Arabic)": "ar",
    "Português (Portuguese)": "pt",
    "Русский (Russian)": "ru",
}

# Static UI strings. Only English + Spanish are hand-written here as a
# baseline; any other selected language falls back to being auto-translated
# once via Gemini and cached in session_state
# (see gemini_client.translate_ui_strings). This keeps the file short while
# still supporting every language in SUPPORTED_LANGUAGES.
UI_STRINGS = {
    "en": {
        "app_title": "🍳 Smart Recipe Assistant",
        "app_subtitle": "Turn what's in your kitchen into delicious, healthy meals — powered by Gemini AI",
        "sidebar_settings": "⚙️ Settings",
        "select_language": "🌐 Select your language",
        "api_key_label": "🔑 Gemini API Key",
        "api_key_help": "Get a free key at aistudio.google.com/apikey",
        "diet_pref": "🥗 Dietary Preference",
        "cuisine_pref": "🌍 Preferred Cuisine",
        "servings": "👥 Servings",
        "allergy_label": "⚠️ Allergies / Ingredients to avoid",
        "tab_ingredients": "🧺 Ingredients",
        "tab_recipes": "🍽️ Recipes",
        "tab_details": "📋 Recipe Details",
        "tab_favorites": "⭐ Favorites",
        "ingredient_input_header": "What do you have?",
        "ingredient_text_label": "Type ingredients (comma separated)",
        "ingredient_upload_label": "📸 Or upload a photo of your ingredients / fridge",
        "detect_button": "🔍 Detect Ingredients from Photo",
        "detected_ingredients": "Detected ingredients",
        "find_recipes_button": "✨ Find Recipes",
        "no_ingredients_warning": "Please add at least one ingredient first.",
        "no_api_key_warning": "Please enter your Gemini API key in the sidebar.",
        "generating_recipes": "Cooking up ideas with Gemini...",
        "match_score": "Match",
        "view_details": "View Details",
        "save_favorite": "Save to Favorites",
        "removed_favorite": "Removed from Favorites",
        "added_favorite": "Added to Favorites!",
        "prep_time": "Prep Time",
        "difficulty": "Difficulty",
        "servings_label": "Servings",
        "ingredients_needed": "Ingredients Needed",
        "instructions": "Instructions",
        "nutrition_header": "🔬 Nutrition Breakdown",
        "shopping_list_header": "🛒 Shopping List",
        "shopping_list_caption": "Ingredients you still need to buy",
        "healthier_header": "💡 Healthier Alternatives",
        "download_shopping_list": "⬇️ Download Shopping List (PDF)",
        "download_recipe": "⬇️ Download Recipe (PDF)",
        "no_favorites": "You haven't saved any recipes yet.",
        "calories": "Calories",
        "protein": "Protein",
        "carbs": "Carbs",
        "fat": "Fat",
        "fiber": "Fiber",
        "footer_note": "AI-generated content — please verify nutrition info for medical or allergy-critical needs.",
        "select_recipe_prompt": "Select a recipe from the Recipes tab to see full details here.",
        "generating_details": "Preparing full recipe details, nutrition & tips...",
    },
    "es": {
        "app_title": "🍳 Asistente Inteligente de Recetas",
        "app_subtitle": "Convierte lo que tienes en la cocina en comidas deliciosas y saludables — con Gemini AI",
        "sidebar_settings": "⚙️ Configuración",
        "select_language": "🌐 Selecciona tu idioma",
        "api_key_label": "🔑 Clave API de Gemini",
        "api_key_help": "Obtén una clave gratis en aistudio.google.com/apikey",
        "diet_pref": "🥗 Preferencia Dietética",
        "cuisine_pref": "🌍 Cocina Preferida",
        "servings": "👥 Porciones",
        "allergy_label": "⚠️ Alergias / Ingredientes a evitar",
        "tab_ingredients": "🧺 Ingredientes",
        "tab_recipes": "🍽️ Recetas",
        "tab_details": "📋 Detalles de la Receta",
        "tab_favorites": "⭐ Favoritos",
        "ingredient_input_header": "¿Qué tienes?",
        "ingredient_text_label": "Escribe los ingredientes (separados por comas)",
        "ingredient_upload_label": "📸 O sube una foto de tus ingredientes / refrigerador",
        "detect_button": "🔍 Detectar Ingredientes de la Foto",
        "detected_ingredients": "Ingredientes detectados",
        "find_recipes_button": "✨ Buscar Recetas",
        "no_ingredients_warning": "Por favor agrega al menos un ingrediente.",
        "no_api_key_warning": "Por favor ingresa tu clave API de Gemini en la barra lateral.",
        "generating_recipes": "Creando ideas con Gemini...",
        "match_score": "Coincidencia",
        "view_details": "Ver Detalles",
        "save_favorite": "Guardar en Favoritos",
        "removed_favorite": "Eliminado de Favoritos",
        "added_favorite": "¡Agregado a Favoritos!",
        "prep_time": "Tiempo de Preparación",
        "difficulty": "Dificultad",
        "servings_label": "Porciones",
        "ingredients_needed": "Ingredientes Necesarios",
        "instructions": "Instrucciones",
        "nutrition_header": "🔬 Desglose Nutricional",
        "shopping_list_header": "🛒 Lista de Compras",
        "shopping_list_caption": "Ingredientes que aún necesitas comprar",
        "healthier_header": "💡 Alternativas Más Saludables",
        "download_shopping_list": "⬇️ Descargar Lista de Compras (PDF)",
        "download_recipe": "⬇️ Descargar Receta (PDF)",
        "no_favorites": "Aún no has guardado ninguna receta.",
        "calories": "Calorías",
        "protein": "Proteína",
        "carbs": "Carbohidratos",
        "fat": "Grasa",
        "fiber": "Fibra",
        "footer_note": "Contenido generado por IA — verifica la información nutricional para necesidades médicas o alergias.",
        "select_recipe_prompt": "Selecciona una receta en la pestaña Recetas para ver los detalles aquí.",
        "generating_details": "Preparando detalles completos, nutrición y consejos...",
    },
}


def get_ui_strings(lang_code: str) -> dict:
    """Return UI string dict for a language code, falling back to English."""
    return UI_STRINGS.get(lang_code, UI_STRINGS["en"])
