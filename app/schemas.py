from pydantic import BaseModel, Field
from typing import List


class PanelOutline(BaseModel):
    panel_number: int
    description: str


class ComicOutline(BaseModel):
    title: str
    panels: List[PanelOutline]


class StoryPanel(BaseModel):
    panel_number: int
    image_prompt: str
    dialogue: str = ""
    narration: str = ""


class ComicStory(BaseModel):
    title: str
    panels: List[StoryPanel] = Field(..., min_length=5, max_length=5)


class PromptRequest(BaseModel):
    story_prompt: str = Field(..., max_length=2000)
    character_name: str
    setting: str
    story_tone: str = "comic"
    art_style: str = "comic book"


class ComicResponse(BaseModel):
    title: str
    panels: List[StoryPanel]
    pdf_url: str