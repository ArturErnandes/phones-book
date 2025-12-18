#Файл с эндпоинтами
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from database import get_subscribers, create_subscriber, PhoneAlreadyExists, SessionDep

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
    name: str
    surnm: str | None = None
    street: str | None = None
    bldng: str | None = None
    bldng_k: str | None = None
    appr: str | None = None
    ph_num: str


@router.post("/new_subscriber", tags=["Абоненты"], summary="Создание нового абонента")
async def new_subscriber(data: AddSubscriber, session: SessionDep):
    print(data.model_dump())
    try:
        subs_id = await create_subscriber(data, session)

        return {"success": True, "subscriber_id": subs_id}

    except PhoneAlreadyExists:
        raise HTTPException(status_code=400, detail="Абонент с таким номером телефона уже существует")

    except Exception:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


