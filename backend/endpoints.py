#Файл с эндпоинтами
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from database import get_subscribers, SessionDep

router = APIRouter()



@router.get("/info", tags=["Главная страница"], summary="Отображения текста на главной странице")
def get_info():
    return {"message": "Телефонный справочник"}


@router.get("/subscribers", tags=["Абоненты"], summary="Получение спииска абонентов")
async def call_subscribers(session: SessionDep):

    subs = await get_subscribers(session)

    return {"data": subs}
