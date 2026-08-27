# 🍳 Smart Recipe Assistant

An AI-powered Streamlit app that turns whatever ingredients you have into
recipe ideas, complete nutrition breakdowns, auto-generated shopping lists,
and healthier ingredient swaps — powered by Google Gemini. Fully
multilingual: pick a language and the entire UI *and* every AI-generated
recipe, nutrition fact, and tip appears in that language.

## ✨ Features

- **📸 Photo ingredient detection** — upload a picture of your fridge or
  pantry and Gemini Vision identifies what's in it.
- **⌨️ Manual ingredient entry** — or just type what you have.
- **🍽️ Smart recipe recommendations** — ranked by ingredient match %,
  filtered by diet (vegan, keto, gluten-free...), cuisine, servings, and
  allergies.
- **📋 Full recipe details** — step-by-step instructions, prep time,
  difficulty.
- **🔬 Nutrition calculator** — calories, protein, carbs, fat, fiber per
  serving.
- **🛒 Auto shopping list** — only the ingredients you're missing, grouped
  by category, downloadable as PDF.
- **💡 Healthier alternatives** — AI-suggested ingredient swaps with the
  health benefit explained.
- **⭐ Favorites** — save recipes for the session.
- **🌐 14 languages** — English, Hindi, Tamil, Telugu, Bengali, Marathi,
  Spanish, French, German, Chinese, Japanese, Arabic, Portuguese, Russian.
  Any language not yet hand-translated is auto-translated on first use.
- **⬇️ PDF export** — download shopping lists and full recipes.

## 🗂️ Project structure

```
smart_recipe_assistant/
├── app.py              # Main Streamlit app (UI + flow)
├── gemini_client.py     # All Gemini API calls (vision + text generation)
├── i18n.py               # Language list + UI translation strings
├── styles.py             # Custom CSS for the polished UI
├── pdf_export.py         # PDF generation for shopping lists & recipes
├── requirements.txt
└── .env.example
```

## 🚀 Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get a free Gemini API key**
   Visit https://aistudio.google.com/apikey and create a key.

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **In the app**: paste your Gemini API key into the sidebar (it's kept
   only in your browser session, never stored to disk), pick your
   language and preferences, then add ingredients via text or photo.

> You can also put your key in a `.env` file (copy `.env.example` to
> `.env`) if you adapt `app.py` to read from `os.environ` — by default
> the app takes the key directly from the sidebar so nothing is
> hard-coded or committed.

## 🧠 How it works

- `gemini_client.py` wraps every Gemini call and always asks the model to
  respond in strict JSON, in the currently selected language — this is
  what lets recipes, nutrition labels, and shopping lists all render
  natively in Hindi, Tamil, Spanish, etc., not just the button labels.
- Recipe recommendation and full-detail generation are separate calls:
  the list view stays fast and cheap, and full nutrition/instructions are
  only generated for the recipe you actually open (cached in
  `st.session_state` so reopening it is instant).
- `styles.py` injects custom CSS so the app doesn't look like default
  Streamlit — gradient hero banner, recipe cards with match-percentage
  bars, badges, and nutrition tiles.

## 💡 Ideas to extend further

- Weekly meal planner that chains multiple recipes and merges their
  shopping lists into one.
- Barcode/receipt scanning to auto-populate the pantry.
- Voice input for hands-free ingredient entry while cooking.
- A "use up leftovers before they expire" mode using expiry dates.
- Persist favorites/pantry to a database (e.g. Supabase) instead of
  session state, with user accounts.

## ⚠️ Note

Nutrition values and recipes are AI-generated estimates. For medical
conditions, allergies, or strict dietary needs, verify with a
professional or trusted nutrition database.
