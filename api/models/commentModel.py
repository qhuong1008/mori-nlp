from pydantic import BaseModel
 
class ClassifiedCommentModel(BaseModel):
    commentText: str
    sentiment: str
