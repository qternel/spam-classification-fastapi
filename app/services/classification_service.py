import re
from typing import Annotated

import spacy
from fastapi import Depends, Request
from sklearn.ensemble import VotingClassifier

from app.db.db import Session
from app.db.db_models import Misclassification
from app.mock_objects.mock_db import MockDB, MockMisclassification
from app.pydantic_models.classification import CollectMisclasificationResponse


def get_classifier(request: Request):
    return request.app.state.classifier


def get_spacy_model(request: Request):
    return request.app.state.spacy_model


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


class ClassificationService:

    def __init__(
        self,
        classifier: Annotated[VotingClassifier, Depends(get_classifier)],
        spacy_model: Annotated[spacy.language.Language, Depends(get_spacy_model)],
        db: Annotated[MockDB, Depends(get_db)],
    ):
        self._classifier = classifier
        self._spacy_model = spacy_model
        self._db = db

    def classify_text(self, text: str):
        return self._classifier.predict([self.normailize_text(text)])[0]

    def collect_misclassification(self, text: str, true_label: bool):
        prediction = self._classifier.predict([self.normailize_text(text)])[0]
        if prediction != true_label:
            mscl = Misclassification(text=text, label=true_label)
            self._db.add(mscl)
            self._db.commit()

        return CollectMisclasificationResponse(
            text=text, true_label=true_label, predicted_label=prediction
        )

    def normailize_text(self, text: str):
        text = text.lower()
        text = re.sub(r"\d+", " ", text)
        text = re.sub(r"\W+", " ", text)
        text = re.sub(r"\s+", " ", text)

        doc = self._spacy_model(text)
        text = " ".join([token.lemma_ for token in doc if not token.is_stop])

        text = re.sub(r"\b\w\b", " ", text)  # single characters
        print(text)
        return text
