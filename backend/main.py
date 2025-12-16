import os

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import uvicorn

from pydantic import BaseModel


load_dotenv()

db_pass = os.getenv("DB_PASS")
db_port = os.getenv("DB_PORT")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_async_engine(f'postgresql+asyncpg://postgres:{db_pass}@localhost:{db_port}/contacts_mai')

new_session = async_sessionmaker(engine, expire_on_commit=False)


