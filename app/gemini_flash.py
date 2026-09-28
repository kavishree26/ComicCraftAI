import json

from google import genai

from .schemas import (
    ComicOutline,
    PanelOutline,
    PromptRequest,
)
from .settings import get_settings


def generate_outline(
    payload: PromptRequest,
) -> ComicOutline:

    settings = get_settings()

    # --------------------------------------------------
    # DEMO MODE
    # Used when GEMINI_API_KEY is empty
    # --------------------------------------------------

    if not settings.gemini_api_key:

        return ComicOutline(
            title=f"{payload.character_name}'s Adventure",
            panels=[
                PanelOutline(
                    panel_number=1,
                    description=(
                        f"{payload.character_name} begins "
                        f"the adventure in {payload.setting}."
                    ),
                ),
                PanelOutline(
                    panel_number=2,
                    description=(
                        f"{payload.character_name} discovers "
                        "something unexpected."
                    ),
                ),
                PanelOutline(
                    panel_number=3,
                    description=(
                        "A challenge appears and the "
                        f"character must take action."
                    ),
                ),
                PanelOutline(
                    panel_number=4,
                    description=(
                        f"{payload.character_name} solves "
                        "the problem."
                    ),
                ),
                PanelOutline(
                    panel_number=5,
                    description=(
                        "The adventure ends with a "
                        "happy conclusion."
                    ),
                ),
            ],
        )

    # --------------------------------------------------
    # GEMINI MODE
    # --------------------------------------------------

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Create a 5-panel comic outline.

Story idea:
{payload.story_prompt}

Main character:
{payload.character_name}

Setting:
{payload.setting}

Story tone:
{payload.story_tone}

Art style:
{payload.art_style}

Create exactly 5 panels.

For every panel provide:
- panel_number
- description

Keep each description short and visual.
"""

    response = client.models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ComicOutline,
        },
    )

    data = json.loads(response.text)

    return ComicOutline.model_validate(data)