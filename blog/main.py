from fastapi import FastAPI #type:ignore

app = FastAPI();

@app.post('/blog')
def createBlog() :
    return 'creating'