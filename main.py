from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users = {
    "franco": {
        "username": "franco",
        "email": "franco@franco.com",
        "password": "password",
    },
    "fabricio": {
        "username": "fabricio",
        "email": "fabricio@fabricio.com",
        "password": "password",
    },
}

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    return user