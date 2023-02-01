from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
app = FastAPI()


class Token(BaseModel):
    token: dict


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

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
