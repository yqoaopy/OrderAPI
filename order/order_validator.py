class ValidationError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

class OrderValidator:
    def __init__(self, strategies):
        self.strategies = strategies

    def validate(self, order: dict):
        for strategy in self.strategies:
            strategy.validate(order)
        return True
