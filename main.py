from fastapi import FastAPI # type: ignore

app = FastAPI()

@app.get('/')
def index() :
    return {'data' : {
        'name' : 'srinjoy'
    }}


@app.get('/about')
def about() :
    return {'data' : {
        'role' : 'SDE'
    }}