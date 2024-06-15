from fastapi import APIRouter, Depends, HTTPException
from api.controllers.recommendationCFController import RecommendationCFController

recommendationCFRouter = APIRouter()
controller = RecommendationCFController()
controller.load_data()

@recommendationCFRouter.get("/user/{user_id}")
def recommend_books_user(user_id: str, n: int = 5):
    try:
        recommended_books = controller.recommend_books_user(user_id, n)
        return {"user_id": user_id, "recommended_books": recommended_books.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recommendationCF: {str(e)}")


@recommendationCFRouter.get("/item/{user_id}")
def recommend_books_item(user_id: str, n: int = 5):
    try:
        recommended_books = controller.recommend_books_item(user_id, n)
        return {"user_id": user_id, "recommended_books": recommended_books.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recommendationCF: {str(e)}")

@recommendationCFRouter.post("/history")
async def recommend_books_based_on_history(request: dict):
    try:
        user_id = request.get("user_id")
        user_history = request.get("user_history")
        n = request.get("n")
        recommendations = controller.recommend_books_based_on_history(user_history, n)
        return {"user_id": user_id, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recommendationCF: {str(e)}")
