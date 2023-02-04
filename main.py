import qrcode
import pyotp
from fastapi import FastAPI, Request, WebSocket, WebSocketException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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