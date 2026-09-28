from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont

from .settings import get_settings


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value)
    return value.strip("_").lower() or "comic"


def generate_image(
    prompt: str,
    filename: str,
    panel_number: int,
) -> str:

    settings = get_settings()

    output_dir = settings.panels_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    # Simple placeholder image for testing
    image = Image.new(
        "RGB",
        (1024, 768),
        "white",
    )

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(
            "arial.ttf",
            32,
        )
    except OSError:
        font = ImageFont.load_default()

    draw.rectangle(
        (20, 20, 1004, 748),
        outline="black",
        width=5,
    )

    draw.text(
        (50, 60),
        f"COMICCRAFT AI - PANEL {panel_number}",
        fill="black",
        font=font,
    )

    # Keep the prompt readable
    short_prompt = prompt[:300]

    draw.text(
        (50, 150),
        short_prompt,
        fill="black",
        font=font,
    )

    image.save(output_path)

    return str(output_path)