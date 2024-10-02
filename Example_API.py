# 1. Library imports
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from IPython.display import Markdown, display



app = FastAPI()



@app.get('/')
def index():
    #add link to documentation
    link = 'http://127.0.0.1:8000/docs'
    content = f'''<h1>Welcome to the example API</h1>
            <h2>Click <a href={link}>here</a> to view the API documentation</h2>
                ''' 
    return HTMLResponse(content=content)   

@app.get('/test')
def test():
    return {'test': 'test', 'value': 'some value'}


@app.get('/additionExample')
def additionExample(a: int, b: int):
    return {'addition': a + b}

@app.get('/subtractionExample')
def subtractionExample(a: int, b: int):
    return {'subtraction': a - b}

@app.get('/multiplicationExample')
def multiplicationExample(a: int, b: int):
    return {'multiplication': a * b}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)