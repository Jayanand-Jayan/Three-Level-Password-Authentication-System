import qrcode
import pyotp
import time
import socket
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/display_qr", response_class=HTMLResponse)
async def display_qr(request: Request):
    global totp
    totp = pyotp.TOTP('base32secret3232')
    totp.interval = 240 
    global query_arg
    query_arg = str(totp.now())

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=3
    )

    qr.add_data("http://"+request.url.hostname+":8000/qr_verify/"+query_arg)   
    qr.make(fit=True)
    img = qr.make_image(fill_color="#E2B144", back_color="#4A171E")
    img.save("static\images\qr.png")

    return templates.TemplateResponse("qr_display.html", {"request": request})

@app.get("/qr_verify/{recv_query_arg}", response_class=HTMLResponse) 
async def qr_verify(request: Request, recv_query_arg: str):
    if totp.verify(recv_query_arg, valid_window=2):
        return templates.TemplateResponse("qr_status.html", {"request": request, "status": "success"})
    else:
        return templates.TemplateResponse("qr_status.html", {"request": request, "status": "failed", "recvarg": recv_query_arg, "queryarg": query_arg})                                                                                                                                                                                                                         

