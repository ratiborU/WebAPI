from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import models
from database import engine
from routes import router_websocket, router_articles, router_comments


models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


app = FastAPI(
    title="WebSocketChatCRUDNotify",
    summary="WebSocket Chat + Notifications of CRUD operations!",
    version="0.0.1",
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    ws_protocol = "wss" if http_protocol == "https" else "ws"
    server_urn = request.url.netloc
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "http_protocol": http_protocol,
                                       "ws_protocol": ws_protocol,
                                       "server_urn": server_urn})


app.include_router(router_websocket)
app.include_router(router_articles)
app.include_router(router_comments)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
