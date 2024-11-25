from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def root() -> JSONResponse:
    return {"message": "Should be working"}
