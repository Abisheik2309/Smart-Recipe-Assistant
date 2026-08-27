"""
pdf_export.py
Generates downloadable PDF files for shopping lists and full recipes
using fpdf2. Uses only core (latin-1 safe) fonts; non-latin text is
transliterated defensively so downloads never crash on unusual
characters — if encoding fails, characters are replaced rather than
raising.
"""

from fpdf import FPDF


def _safe(text: str) -> str:
    if text is None:
        return ""
    return str(text).encode("latin-1", "replace").decode("latin-1")


def build_shopping_list_pdf(recipe_title: str, shopping_list: list, ui_strings: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(255, 106, 136)
    pdf.cell(0, 12, _safe(ui_strings.get("shopping_list_header", "Shopping List")), ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 8, _safe(f"{recipe_title}"), ln=True)
    pdf.ln(4)

    pdf.set_draw_color(220, 220, 220)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(90, 9, "Item", border="B")
    pdf.cell(45, 9, "Quantity", border="B")
    pdf.cell(55, 9, "Category", border="B", ln=True)

    pdf.set_font("Helvetica", "", 11)
    for entry in shopping_list:
        pdf.cell(90, 9, _safe(entry.get("item", "")), border="B")
        pdf.cell(45, 9, _safe(entry.get("quantity", "")), border="B")
        pdf.cell(55, 9, _safe(entry.get("category", "")), border="B", ln=True)

    return bytes(pdf.output())


def build_recipe_pdf(recipe_detail: dict, ui_strings: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(255, 106, 136)
    pdf.multi_cell(0, 12, _safe(recipe_detail.get("title", "")), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Metadata
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(90, 90, 90)
    meta = f"{ui_strings.get('prep_time','Prep Time')}: {recipe_detail.get('prep_time_minutes','?')} min   |   " \
           f"{ui_strings.get('difficulty','Difficulty')}: {recipe_detail.get('difficulty','')}   |   " \
           f"{ui_strings.get('servings_label','Servings')}: {recipe_detail.get('servings','')}"
    pdf.multi_cell(0, 8, _safe(meta), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Ingredients Needed
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 10, _safe(ui_strings.get("ingredients_needed", "Ingredients")), ln=True)
    pdf.set_font("Helvetica", "", 11)
    for ing in recipe_detail.get("full_ingredient_list", []):
        pdf.set_x(pdf.l_margin)  # Ensure cursor is reset to the left margin
        line = f"- {ing.get('name','')} ({ing.get('quantity','')})"
        pdf.multi_cell(0, 7, _safe(line), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Instructions
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, _safe(ui_strings.get("instructions", "Instructions")), ln=True)
    pdf.set_font("Helvetica", "", 11)
    for i, step in enumerate(recipe_detail.get("instructions", []), start=1):
        pdf.set_x(pdf.l_margin)  # Ensure cursor is reset to the left margin
        pdf.multi_cell(0, 7, _safe(f"{i}. {step}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Nutrition
    nutrition = recipe_detail.get("nutrition", {})
    if nutrition:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, _safe(ui_strings.get("nutrition_header", "Nutrition")), ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_x(pdf.l_margin)
        n_line = (
            f"{ui_strings.get('calories','Calories')}: {nutrition.get('calories_kcal','?')} kcal   "
            f"{ui_strings.get('protein','Protein')}: {nutrition.get('protein_g','?')} g   "
            f"{ui_strings.get('carbs','Carbs')}: {nutrition.get('carbs_g','?')} g   "
            f"{ui_strings.get('fat','Fat')}: {nutrition.get('fat_g','?')} g   "
            f"{ui_strings.get('fiber','Fiber')}: {nutrition.get('fiber_g','?')} g"
        )
        pdf.multi_cell(0, 7, _safe(n_line), new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
