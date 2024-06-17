from fastapi import APIRouter, Depends, HTTPException
from concurrent.futures import ThreadPoolExecutor
from api.controllers.recommendationCBController import RecommendationCBController

recommendationCBRouter = APIRouter()
controller = RecommendationCBController()

@recommendationCBRouter.post('/create-recommend')
async def recommendations(request: dict):
    try:
        all_books = request.get("allBooks")

        recommendations = controller.generate_recommendations(all_books)

        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recommendationCF: {str(e)}")

