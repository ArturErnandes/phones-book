#Файл с эндпоинтами
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

router = APIRouter()



@router.get("/info", tags=["Главная страница"], summary="Отображения текста на главной странице")
def get_info():
    return {"message": "Телефонный справочник"}


@router.get("/subscribers", tags=["Абоненты"], summary="Получение спииска абонентов")
def get_subscribers():
    ...

    return {"success": True}
