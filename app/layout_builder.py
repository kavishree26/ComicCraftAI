from dataclasses import dataclass
from typing import List

from .schemas import ComicStory


@dataclass
class ComicPanel:
    panel_number: int
    image_url: str
    dialogue: str
    narration: str


def build_comic_layout(
    image_urls: List[str],
    story: ComicStory,
) -> List[ComicPanel]:

    layout = []

    for index, panel in enumerate(story.panels):
        image_url = (
            image_urls[index]
            if index < len(image_urls)
            else ""
        )

        layout.append(
            ComicPanel(
                panel_number=panel.panel_number,
                image_url=image_url,
                dialogue=panel.dialogue,
                narration=panel.narration,
            )
        )

    return layout