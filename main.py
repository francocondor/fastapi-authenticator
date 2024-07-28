from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from jose import jwt

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

def encode_token(payload: dict)-> str:
    token = jwt.encode(payload, "my-secret", algorithm="HS256")
    return token

def decode_token(token: Annotated[str, Depends(oauth2_scheme)])-> dict:
    data = jwt.decode(token, "my-secret", algorithms=["HS256"])
    users.get(data["username"])
    return data

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return {"access_token": token}

@app.get("/users/profile")
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user