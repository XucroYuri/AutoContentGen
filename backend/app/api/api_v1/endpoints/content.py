
from fastapi import APIRouter, Depends, HTTPException
from app.services.content_service import ContentService
from app.schemas.content import ContentCreate, ContentResponse
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=ContentResponse)
async def generate_content(topic: str):
    try:
        content_service = ContentService()
        result = await content_service.generate_content(topic)
        return result
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))