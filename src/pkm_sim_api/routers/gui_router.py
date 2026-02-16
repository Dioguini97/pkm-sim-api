# gui.py
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent

router = APIRouter(prefix="/gui", tags=["GUI"])
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@router.get("/ability", response_class=HTMLResponse)
async def ability_editor(request: Request):
    return templates.TemplateResponse("ability.html", {"request": request})

@router.get("/item", response_class=HTMLResponse)
async def item_editor(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})

@router.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/tab/{tab_name}")
async def load_tab(request: Request, tab_name: str):
    allowed = ["pokemon", "move", "item", 'ability']

    if tab_name not in allowed:
        return {"error": "Invalid tab"}

    return templates.TemplateResponse(
        f"{tab_name}.html",
        {"request": request}
    )
