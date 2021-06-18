from pathlib import Path
from hmac import compare_digest
from os import getenv

from aiofiles import open
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, File
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles


load_dotenv()

Path("./images").mkdir(exist_ok=True)

app = FastAPI(openapi_url=None)
app.mount("/i", StaticFiles(directory="./images"), "images")

@app.post("/upload/{name}")
async def upload(name: str, request: Request, file: bytes = File(...)) -> Response:
    if not compare_digest(request.headers.get("Authorization", ""), getenv("TOKEN")):
        raise HTTPException(401)

    with Path(f"./images/{name}.png").open("wb") as f:
        f.write(file)

    return Response(status_code=204)
