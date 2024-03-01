import uvicorn
from fastapi import FastAPI



app = FastAPI()



@app.get('/', response_model=str)
def say_hello():
    return 'Hello!'



if __name__ == '__main__':
    uvicorn.run(app)
