from transformers import pipeline

from api.schemas.commentSchema import ClassifiedCommentResponseModel
from api.services.commentService import CommentService

pipe = pipeline("text-classification", model="toiquangle1234/comment_classification")

class CommentController:
  def __init__(self):
    pass

  def commentClassification(self, text: str):
    commentService = CommentService()
    classifyResult: ClassifiedCommentResponseModel = commentService.commentClassificationHandler(text)
    return classifyResult
