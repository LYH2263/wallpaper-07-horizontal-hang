from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.engines.wallpaper_math import ORIENTATIONS
from app.repositories import settings_repo

router = APIRouter()


class SettingValue(BaseModel):
    value: str


@router.get("/settings")
def settings():
    return settings_repo.get_all()


@router.put("/settings/{key}")
def set_setting(key: str, body: SettingValue):
    if key == "default_orientation" and body.value not in ORIENTATIONS:
        raise HTTPException(422, "invalid orientation")
    settings_repo.set_value(key, body.value)
    return settings_repo.get_all()
