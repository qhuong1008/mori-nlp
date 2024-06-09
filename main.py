import uvicorn
from fastapi import FastAPI
from api.routes.commentRouter import commentRouter

app = FastAPI()
app.include_router(commentRouter, prefix="/nlp/comment")

def root():
    uvicorn.run("main:app", host="0.0.0.0", port=8000)