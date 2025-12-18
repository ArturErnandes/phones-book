#Файл с функционалом взаимодействия с БД

import os

from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text

from fastapi import Depends

from typing import Annotated


load_dotenv()

db_admin = os.getenv("DB_ADMIN")
db_pass = os.getenv("DB_PASS")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


engine = create_async_engine(f'postgresql+asyncpg://{db_admin}:{db_pass}@localhost:{db_port}/{db_name}')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_subscribers_db(session: AsyncSession):
    query = text("""
        SELECT
            s.subs_id,
            f.fam_value       AS fam,
            n.name_value      AS name,
            sn.snm_value      AS surnm,
            st.street_value   AS street,
            s.bldng,
            s.bldng_k,
            s.appr,
            s.ph_num
        FROM subscribers s
        JOIN fams f ON s.fam = f.fam_id
        JOIN names n ON s.name_ = n.name_id
        LEFT JOIN surnames sn ON s.surnm = sn.snm_id
        LEFT JOIN streets st ON s.street = st.street_id
        ORDER BY s.subs_id
    """)

    result = await session.execute(query)

    rows = result.mappings().all()

    return [dict(row) for row in rows]


class PhoneAlreadyExists(Exception):
    pass


async def new_subscriber_db(data, session: AsyncSession) -> int:
    async with session.begin():

        exists = await session.execute(text("SELECT 1 FROM subscribers WHERE ph_num = :ph"),

            {"ph": data.ph_num})
        if exists.first():
            raise PhoneAlreadyExists()

        async def resolve_id(table, id_col, value_col, value):
            if value is None:
                return None

            insert_result = await session.execute(
                text(f"""INSERT INTO {table} ({value_col}) VALUES (lower(trim(:v))) ON CONFLICT ({value_col}) DO NOTHING RETURNING {id_col}"""),

                {"v": value})

            inserted_row = insert_result.first()
            if inserted_row:
                return inserted_row[0]

            select_result = await session.execute(
                text(f"""SELECT {id_col} FROM {table} WHERE {value_col} = lower(trim(:v))"""),

                {"v": value})

            return select_result.scalar_one()

        fam_id = await resolve_id("fams", "fam_id", "fam_value", data.fam)
        name_id = await resolve_id("names", "name_id", "name_value", data.name)
        surnm_id = await resolve_id("surnames", "snm_id", "snm_value", data.surnm)
        street_id = await resolve_id("streets", "street_id", "street_value", data.street)

        result = await session.execute(
            text("""
                INSERT INTO subscribers (fam, name_, surnm, street, bldng, bldng_k, appr, ph_num)
                VALUES (:fam, :name, :surnm, :street, :bldng, :bldng_k, :appr, :ph_num)
                RETURNING subs_id"""),

            {
                "fam": fam_id,
                "name": name_id,
                "surnm": surnm_id,
                "street": street_id,
                "bldng": data.bldng,
                "bldng_k": data.bldng_k,
                "appr": data.appr,
                "ph_num": data.ph_num,
            }
        )

        return result.scalar_one()


async def delete_subscriber_db(subs_id, session: AsyncSession):
    async with session.begin():
        await session.execute(text("""DELETE FROM subscribers WHERE subs_id = :subs_id RETURNING subs_id"""),{"subs_id": subs_id})


async def search_subscribers_db(
    session: AsyncSession,
    fam: str | None = None,
    name: str | None = None,
    surnm: str | None = None,
    street: str | None = None,
) -> list[dict]:

    conditions = []
    params = {}

    if fam:
        conditions.append("f.fam_value = lower(trim(:fam))")
        params["fam"] = fam

    if name:
        conditions.append("n.name_value = lower(trim(:name))")
        params["name"] = name

    if surnm:
        conditions.append("sn.snm_value = lower(trim(:surnm))")
        params["surnm"] = surnm

    if street:
        conditions.append("st.street_value = lower(trim(:street))")
        params["street"] = street

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query = f"""
        SELECT
            s.subs_id,
            f.fam_value      AS fam,
            n.name_value     AS name,
            sn.snm_value     AS surnm,
            st.street_value  AS street,
            s.bldng,
            s.bldng_k,
            s.appr,
            s.ph_num
        FROM subscribers s
        JOIN fams f ON s.fam = f.fam_id
        JOIN names n ON s.name_ = n.name_id
        LEFT JOIN surnames sn ON s.surnm = sn.snm_id
        LEFT JOIN streets st ON s.street = st.street_id
        {where_clause}
        ORDER BY s.subs_id
    """

    result = await session.execute(text(query), params)
    return [dict(row) for row in result.mappings().all()]
