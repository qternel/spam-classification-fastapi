from typing import Annotated

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: Annotated[str, Field(min_length=1)]


class ClassificationResponse(TextRequest):
    is_spam: bool


class CollectMisclassificationRequest(BaseModel):
    text: Annotated[str, Field(min_length=1)]
    true_label: bool


class CollectMisclasificationResponse(CollectMisclassificationRequest):
    predicted_label: bool
