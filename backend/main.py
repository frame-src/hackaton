from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import router  
from const.const import DESCRIPTION, NAME, TITLE

def app() -> FastAPI:

    app = FastAPI(
        title=TITLE,
        docs_url="/{NAME}/docs",
        debug=False,
        description=DESCRIPTION,
        openapi_url="/{NAME}/openapi.json"
    )

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    
    return app

app()


@app.get("/")
def root():
    return {"message": "{TITLE} works"}
