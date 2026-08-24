from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.pydantic_models.classification import ClassificationResponse, TextRequest
from app.services.classification_service import ClassificationService

router = APIRouter()


@router.post(
    "/classify", status_code=status.HTTP_200_OK, response_model=ClassificationResponse
)
async def classify_text(
    text_request: TextRequest,
    classification_service: Annotated[ClassificationService, Depends()],
):
    text = text_request.text

    return ClassificationResponse(
        text=text, is_spam=classification_service.classify_text(text)
    )
