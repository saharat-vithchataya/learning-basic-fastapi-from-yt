from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import router


def create_table():
    from database import engine
    import models

    models.Base.metadata.create_all(bind=engine)


def get_application():
    app = FastAPI()
    app.include_router(router=router, prefix="/api")
    app.middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = get_application()
