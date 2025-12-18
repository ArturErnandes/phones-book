#Файл с эндпоинтами
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from database import get_subscribers_db, new_subscriber_db, delete_subscriber_db, PhoneAlreadyExists, SessionDep

router = APIRouter()



@router.get("/info", tags=["Главная страница"], summary="Отображения текста на главной странице")
def get_info():
    return {"message": "Телефонный справочник"}


@router.get("/subscribers", tags=["Абоненты"], summary="Получение спииска абонентов")
async def get_subscribers(session: SessionDep):

    subs = await get_subscribers_db(session)

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
        subs_id = await new_subscriber_db(data, session)

        return {"success": True, "subscriber_id": subs_id}

    except PhoneAlreadyExists:
        raise HTTPException(status_code=400, detail="Абонент с таким номером телефона уже существует")

    except Exception:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.delete("/subscribers/{subs_id}", tags=["Абоненты"], summary="Удаление абонента")
async def delete_subscriber(subs_id: int, session: SessionDep):
    try:
        await delete_subscriber_db(subs_id, session)
        return {"success": True}
    except Exception as e:
        return {"Ошибка при удалении абонента": str(e)}
