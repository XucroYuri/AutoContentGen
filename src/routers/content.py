from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.content import ContentRequest, ContentResponse
from ..core.pipeline import ContentPipeline
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/content", tags=["content"])
pipeline = ContentPipeline()

@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    request: ContentRequest,
    current_user = Depends(get_current_user)
):
    try:
        result = await pipeline.generate_async(request.prompt)
        return ContentResponse(
            status="success",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[ContentResponse])
async def get_history(
    current_user = Depends(get_current_user)
):
    try:
        history = await pipeline.get_user_history(current_user.id)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
