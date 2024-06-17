import uvicorn
from fastapi import FastAPI
from api.routes.commentRouter import commentRouter
from api.routes.recommendationRouter import recommendationCFRouter
from api.routes.recommendationCBRouter import recommendationCBRouter

app = FastAPI()
app.include_router(commentRouter, prefix="/nlp/comment")
app.include_router(recommendationCFRouter, prefix="/nlp/recommend")
app.include_router(recommendationCBRouter, prefix="/nlp/recommendcb")

def root():
    uvicorn.run("main:app", host="0.0.0.0", port=8000)