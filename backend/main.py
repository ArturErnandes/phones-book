import os
import uvicorn

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints import router


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

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)