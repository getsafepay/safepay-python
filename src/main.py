from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import json

app = FastAPI()


class Token(BaseModel):
    sig: dict
    data: dict


@app.get("/my-first-api")
def hello(name=None):

    if name is None:
        text = 'Hello!'

    else:
        text = 'Hello ' + name + '!'

    return text


@app.post("/webhook")
def get_token(token: Token):

    if token is None:
        token = "None"

    else:
        token = token

    return token
