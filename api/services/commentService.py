
from transformers import pipeline
from api.schemas.commentSchema import ClassifiedCommentResponseModel

class CommentService:
  def __init__(self):
    pass
  def commentClassificationHandler(self, text):
    pipe = pipeline("text-classification", model="toiquangle1234/comment_classification")
    # text = "Sách in rất tệ, giấy kém chất lượng, bìa yếu ớt. Thật là lãng phí tiền bạc khi mua cuốn sách này."
    result = pipe(text)
    classifiedResult = ClassifiedCommentResponseModel(text=text,sentiment=result[0]['label'])

    return classifiedResult
    