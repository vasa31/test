from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    message: str

# Разрешаем запросы с любого источника (для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Словарь команд и ответов
commands = {
    "привет": "Привет! Как я могу помочь?",
    "как дела": "У меня всё хорошо, спасибо! А у вас?",
    "пока": "До свидания! Хорошего дня!",
    "что такое SuperApp": "SuperApp — это мобильное приложение, которое объединяет в себе множество различных сервисов и функций."
}

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(msg: Message):
    user_message = msg.message.lower()
    response = commands.get(user_message, "Извините, я не понимаю эту команду.")
    return {"response": response}