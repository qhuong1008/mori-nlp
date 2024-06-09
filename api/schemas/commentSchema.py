from pydantic import BaseModel

class CommentInputModel(BaseModel):
    text: str

class ClassifiedCommentResponseModel(BaseModel):
    text: str
    sentiment: str
