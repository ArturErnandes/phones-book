#Файл с функционалом взаимодействия с БД

import os

from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text

from fastapi import Depends

from typing import Annotated


load_dotenv()

db_pass = os.getenv("DB_PASS")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


engine = create_async_engine(f'postgresql+asyncpg://postgres:{db_pass}@localhost:{db_port}/{db_name}')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_subscribers(session: AsyncSession):
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


async def create_subscriber(data, session: AsyncSession):
    ...