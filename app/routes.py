from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .exporters import save_pdf
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import (
    generate_image,
    sanitize_filename,
)
from .layout_builder import (
    build_comic_layout,
)
from .schemas import (
    ComicResponse,
    PromptRequest,
)
from .settings import get_settings


router = APIRouter()

settings = get_settings()

templates = Jinja2Templates(
    directory=str(
        settings.templates_dir
    )
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    story_tone: str = Form("comic"),
    art_style: str = Form("comic book"),
):

    try:

        payload = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            story_tone=story_tone,
            art_style=art_style,
        )

        # -------------------------
        # STEP 1
        # Generate outline
        # -------------------------

        outline = generate_outline(
            payload
        )

        # -------------------------
        # STEP 2
        # Generate story
        # -------------------------

        story = generate_story(
            payload,
            outline,
        )

        # -------------------------
        # STEP 3
        # Generate images
        # -------------------------

        image_urls = []

        character_filename = (
            sanitize_filename(
                payload.character_name
            )
        )

        for panel in story.panels:

            filename = (
                f"panel_"
                f"{panel.panel_number}_"
                f"{character_filename}.png"
            )

            generate_image(
                panel.image_prompt,
                filename,
                panel.panel_number,
            )

            image_urls.append(
                "/static/panels/"
                + filename
            )

        # -------------------------
        # STEP 4
        # Build layout
        # -------------------------

        layout = build_comic_layout(
            image_urls,
            story,
        )

        # -------------------------
        # STEP 5
        # Create PDF
        # -------------------------

        pdf_url = save_pdf(
            layout,
            story.title,
        )

        # -------------------------
        # STEP 6
        # Render preview
        # -------------------------

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "story": story,
                "layout": layout,
                "pdf_url": pdf_url,
            },
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.post(
    "/generate-comic/json",
    response_model=ComicResponse,
)
async def generate_comic_json(
    payload: PromptRequest,
):

    try:

        outline = generate_outline(
            payload
        )

        story = generate_story(
            payload,
            outline,
        )

        image_urls = []

        character_filename = (
            sanitize_filename(
                payload.character_name
            )
        )

        for panel in story.panels:

            filename = (
                f"panel_"
                f"{panel.panel_number}_"
                f"{character_filename}.png"
            )

            generate_image(
                panel.image_prompt,
                filename,
                panel.panel_number,
            )

            image_urls.append(
                "/static/panels/"
                + filename
            )

        layout = build_comic_layout(
            image_urls,
            story,
        )

        pdf_url = save_pdf(
            layout,
            story.title,
        )

        return ComicResponse(
            title=story.title,
            panels=story.panels,
            pdf_url=pdf_url,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
    pdf_url: str = "/",
):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "pdf_url": pdf_url,
        },
    )


@router.get("/test-image")
async def test_image(
    prompt: str = (
        "A friendly explorer discovering "
        "a magical forest, comic book art"
    ),
):

    filename = "test_panel.png"

    path = generate_image(
        prompt,
        filename,
        1,
    )

    return {
        "ok": True,
        "image_url": (
            "/static/panels/"
            + filename
        ),
        "path": path,
    }