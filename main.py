import qrcode
import pyotp
import google
import jwt
from fastapi import FastAPI, Request, WebSocket, WebSocketException, Form, Depends, HTTPException, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session 
from typing import Annotated
import crud, models, schemas
from database import SessionLocal, engine
import bcrypt

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

CLIENT_ID = "229587252978-th5hq1fqapnei7cs2jq1hjj800tmb9co.apps.googleusercontent.com"
SECRET_KEY = "1aae8d7c92058b5eea456895bf89084571e306f3"
ALGORITHM = "RS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()


@app.get("/login") 
async def display_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup")
async def display_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/register")
def register(request: Request, username: str = Form(), password: str = Form(), mail: str = Form(), phno: str = Form(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username)
    if db_user is not None:
        raise HTTPException(status_code=403, detail="User already exists")
    
    new_user = schemas.UserCreate(username=username, password=password, mail=mail, phno=phno)
    new_user = crud.create_user(db, new_user)

    return {"authorized": True, "name": new_user.username}



@app.post("/verify")
def login(request: Request, username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(password.encode('utf-8'), db_user.hashed_pwd.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Unauthorized user")

    return RedirectResponse("http://localhost/otp-ver/index.php")


@app.get("/display_qr", response_class=HTMLResponse)
def display_qr(request: Request):
    global totp
    totp = pyotp.TOTP('base32secret3232')
    totp.interval = 240 
    global query_arg
    query_arg = str(totp.now())

    return templates.TemplateResponse("qr_display.html", {"request": request, "totp": query_arg })

connected_client = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    connected_client.add(websocket)
    await websocket.accept()
    try:
        while True: 
            data = await websocket.receive_text()
            print("My data is: ", data)
            if data == query_arg:
                for client in connected_client:
                    await client.send_text("Authenticated")
    finally:
        connected_client.remove(websocket)    
