import random


class MockClassifier:

    def predict(self, text: str):
        r = random.random()
        if r < 0.5:
            return False
        return True
