import time

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


@app.get('/', response_model=str)
def say_hello():
    return 'Hello!'


def job():
    for i in range(10):
        print(i)
        time.sleep(1)



# @app.get('/test')
# def test_bg_task(smth: Model = Depends()):
#     return smth


if __name__ == '__main__':
    uvicorn.run(app)
