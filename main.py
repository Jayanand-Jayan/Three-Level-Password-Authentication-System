import qrcode
import pyotp
from fastapi import FastAPI, Request, WebSocket, WebSocketException, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session 
import crud, models, schemas
from database import SessionLocal, engine
import bcrypt

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()

@app.get("/display_qr", response_class=HTMLResponse)
def display_qr(request: Request):
    global totp
    totp = pyotp.TOTP('base32secret3232')
    totp.interval = 240 
    global query_arg
    query_arg = str(totp.now())

    return templates.TemplateResponse("qr_display.html", {"request": request, "totp": query_arg })

@app.get("/login") 
async def display_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/verify")
def login(request: Request, username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    
    return {"authorized": True, "name": db_user.name}

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