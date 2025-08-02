from fastapi import APIRouter
from app.core.rag_learner import get_rag_learner

router = APIRouter()

@router.get("/learning/stats")
async def get_learning_statistics():
    """Get RAG learning system statistics"""
    try:
        rag_learner = await get_rag_learner()
        stats = rag_learner.get_learning_statistics()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/learning/reset")
async def reset_learning_statistics():
    """Reset learning statistics (for testing)"""
    try:
        rag_learner = await get_rag_learner()
        rag_learner.learning_stats = {}
        return {
            "success": True,
            "message": "Learning statistics reset"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
