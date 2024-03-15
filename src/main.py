from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Server starts')
    yield
    print('Server stops')

app = FastAPI(
    title='FamilyTasker',
    lifespan=lifespan
             )
app.include_router(router)

@app.get('/')
def say_hello():
    return 'Hello!'


if __name__ == '__main__':
    uvicorn.run(app, reload=False)
