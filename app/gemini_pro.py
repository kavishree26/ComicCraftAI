import json
from google import genai

from .schemas import ComicOutline, ComicStory, PromptRequest
from .settings import get_settings


def generate_story(
    payload: PromptRequest,
    outline: ComicOutline,
) -> ComicStory:

    settings = get_settings()

    # Demo mode when Gemini API key is empty
    if not settings.gemini_api_key:
        panels = []

        for panel in outline.panels:
            panels.append(
                {
                    "panel_number": panel.panel_number,
                    "image_prompt": (
                        f"{panel.description}, "
                        f"{payload.art_style}, "
                        f"comic book illustration"
                    ),
                    "dialogue": (
                        f"{payload.character_name}: "
                        "What an amazing adventure!"
                    ),
                    "narration": panel.description,
                }
            )

        return ComicStory(
            title=outline.title,
            panels=panels,
        )

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Create the complete dialogue and narration
for this 5-panel comic.

Character: {payload.character_name}
Setting: {payload.setting}
Tone: {payload.story_tone}
Art style: {payload.art_style}

Story outline:
{json.dumps(outline.model_dump(), indent=2)}

Return exactly 5 panels.

For every panel provide:
- panel_number
- image_prompt
- dialogue
- narration
"""

    response = client.models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ComicStory,
        },
    )

    data = json.loads(response.text)

    return ComicStory.model_validate(data)