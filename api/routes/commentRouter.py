from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from api.controllers.commentController import CommentController
from api.schemas.commentSchema import ClassifiedCommentResponseModel, CommentInputModel

commentRouter = APIRouter()

@commentRouter.post("/classify",response_model=ClassifiedCommentResponseModel)
async def commentClassify(payload: CommentInputModel)->Any:
    try:
        commentController = CommentController()
        data: ClassifiedCommentResponseModel = commentController.commentClassification(payload.text)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error classifying comment: {str(e)}")
    
@commentRouter.get("/hi")
async def sayHi():
    return 'hello'