import uvicorn
from fastapi import FastAPI
from api.routes.commentRouter import commentRouter
from api.routes.recommendationRouter import recommendationCFRouter

app = FastAPI()
app.include_router(commentRouter, prefix="/nlp/comment")
app.include_router(recommendationCFRouter, prefix="/nlp/recommend")

def root():
    uvicorn.run("main:app", host="0.0.0.0", port=8000)