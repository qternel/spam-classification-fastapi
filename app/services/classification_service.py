import re
from typing import Annotated

import spacy
from fastapi import Depends, Request
from sklearn.ensemble import VotingClassifier


def get_classifier(request: Request):
    return request.app.state.classifier


def get_spacy_model(request: Request):
    return request.app.state.spacy_model


class ClassificationService:

    def __init__(
        self,
        classifier: Annotated[VotingClassifier, Depends(get_classifier)],
        spacy_model: Annotated[spacy.language.Language, Depends(get_spacy_model)],
    ):
        self._classifier = classifier
        self._spacy_model = spacy_model

    def classify_text(self, text):
        return self._classifier.predict([self.normailize_text(text)])[0]

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
