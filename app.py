from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from config.settings import Settings
from src.controllers.user_controller import router as user_router
from src.controllers.auth_controller import router as auth_router
from src.controllers.donor_controller import router as donor_router
from src.service.session import setup_db
import sys


engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


async def lifespan(app: FastAPI):
    try:
        setup_db()
    except Exception as e:
        print(e)
        sys.exit(1)
    yield


app = FastAPI(
    title='givelink-api',
    description='GiveLink API reference.',
    version='0.0.1',
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(donor_router)


@app.get("/")
def root(): 
    return {"message": "Hello world!"}
