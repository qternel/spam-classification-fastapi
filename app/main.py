from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import spacy
from fastapi import FastAPI

from app.db.db import Base, engine
from app.mock_objects.mock_classifier import MockClassifier
from app.routes import classification


@asynccontextmanager
async def lifespan(app: FastAPI):
    path = (
        Path(__file__).resolve().parent.parent / "models" / "voting_classifier.joblib"
    )
    app.state.spacy_model = spacy.load("en_core_web_md")
    app.state.classifier = joblib.load(path)
    # app.state.classifier = MockClassifier()
    yield


app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(engine)

app.include_router(classification.router)
