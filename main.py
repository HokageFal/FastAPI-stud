from fastapi import FastAPI, WebSocket, Request
from users.routers.user import router as users_router
from channels.routers.channel import router as channels_router
from starlette.websockets import WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from users.routers.user import router as websocket_router
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки можно разрешить все origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")
app.include_router(users_router, )
app.include_router(channels_router, )
app.include_router(websocket_router, )
ALGORITHM = 'HS256'

@app.get("/websocket",  response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect as e:
        print(f'Connection closed {e.code}')