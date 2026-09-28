from pathlib import Path

from fpdf import FPDF

from .layout_builder import ComicPanel
from .settings import get_settings


def save_pdf(
    layout: list[ComicPanel],
    title: str,
) -> str:

    settings = get_settings()

    export_dir = settings.exports_dir
    export_dir.mkdir(parents=True, exist_ok=True)

    safe_title = "".join(
        character
        for character in title
        if character.isalnum() or character in " _-"
    ).strip()

    if not safe_title:
        safe_title = "comic"

    pdf_path = export_dir / f"{safe_title}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    for panel in layout:
        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            16,
        )

        pdf.cell(
            0,
            10,
            f"Panel {panel.panel_number}",
            ln=True,
        )

        image_path = _image_path_from_url(
            panel.image_url,
            settings.panels_dir,
        )

        if image_path.exists():
            pdf.image(
                str(image_path),
                x=15,
                y=30,
                w=180,
            )

        pdf.ln(125)

        pdf.set_font(
            "Helvetica",
            "",
            12,
        )

        if panel.narration:
            pdf.multi_cell(
                0,
                8,
                f"Narration: {panel.narration}",
            )

        if panel.dialogue:
            pdf.multi_cell(
                0,
                8,
                f"Dialogue: {panel.dialogue}",
            )

    pdf.output(str(pdf_path))

    return "/static/exports/" + pdf_path.name


def _image_path_from_url(
    image_url: str,
    panels_dir: Path,
) -> Path:

    filename = image_url.rsplit(
        "/",
        1,
    )[-1]

    return panels_dir / filename