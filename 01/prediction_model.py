class SomeModel:
    def predict(self, message: str) -> float:
        # реализация не важна
        pass


def predict_message_mood(
        message: str,
        bad_thresholds: float = 0.3,
        good_thresholds: float = 0.8,
) -> str:
    if (good_thresholds <= bad_thresholds or
            bad_thresholds < 0 or
            good_thresholds > 1):
        raise ValueError('Incorrect thresholds')
    model = SomeModel()
    prediction = model.predict(message)
    if not prediction:
        raise ValueError('No prediction')
    if prediction < 0 or prediction > 1:
        raise ValueError('Prediction not between 0 and 1')
    if prediction < bad_thresholds:
        return 'неуд'
    if prediction > good_thresholds:
        return 'отл'
    return 'норм'