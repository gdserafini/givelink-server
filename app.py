from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from config.settings import Settings


engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


async def lifespan(app: FastAPI):
    try:
        with engine.connect() as connection:
            print(f'Successfully connection: {connection}')
            inspector = inspect(engine)
            #if 'users' not in inspector.get_table_names():
            #    print('Not found db tables, running migrations...')
            #    subprocess.run(['alembic', 'upgrade', 'head'], check=True)
            #    print('Finished migrations.')
    except Exception as e:
        detail = f'Database connection error: {e}'
        raise Exception(message=detail)
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root(): 
    return {"message": "Hello world!"}
