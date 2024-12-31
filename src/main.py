"""
    Создание основного приложения FastAPI,
    подключение всех роутеров,
    запуск предварительных и завершающих команд
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from src.layers.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    """'Обертка' для реализации событий до и после запуска приложения"""
    print("Server starts")
    yield
    print("Server stops")


app = FastAPI(
    title="FamilyTasker",
    description="Multi-person ToDoList with registration, authentication, notifications, rating system.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
def say_hello():
    """Тестовое сообщение для проверки работоспособности приложения"""
    return "Hello!"


if __name__ == "__main__":
    uvicorn.run(app, reload=False)
