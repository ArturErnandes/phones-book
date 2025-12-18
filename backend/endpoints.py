#Файл с эндпоинтами
from fastapi import APIRouter

from pydantic import BaseModel

from database import get_subscribers, create_subscriber, SessionDep

router = APIRouter()



@router.get("/info", tags=["Главная страница"], summary="Отображения текста на главной странице")
def get_info():
    return {"message": "Телефонный справочник"}


@router.get("/subscribers", tags=["Абоненты"], summary="Получение спииска абонентов")
async def call_subscribers(session: SessionDep):

    subs = await get_subscribers(session)

    return {"data": subs}


class AddSubscriber(BaseModel):
    fam: str
    name_: str
    surnm: str | None = None
    street: str | None = None
    bldng: str | None = None
    bldng_k: str | None = None
    appr: str | None = None
    ph_num: str


@router.post("/new_subscriber", tags=["Абоненты"], summary="Создание нового абонента")
async def new_sub(data: AddSubscriber, session: SessionDep):

    await create_subscriber(data, session)

    return {"success": True}

