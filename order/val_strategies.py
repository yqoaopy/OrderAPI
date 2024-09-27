from order.order_validator import ValidationError


class ValidationStrategy:
    def validate(self, order: dict):
        raise NotImplementedError("Subclasses should implement this method")

class NameValidationStrategy(ValidationStrategy):
    def validate(self, order: dict):
        if not order["name"].isalpha():
            raise ValidationError(400, "Name contains non-English characters")
        if not order["name"][0].isupper():
            raise ValidationError(400, "Name is not capitalized")

class PriceValidationStrategy(ValidationStrategy):
    def validate(self, order: dict):
        if int(order["price"]) > 2000:
            raise ValidationError(400, "Price is over 2000")

class CurrencyValidationStrategy(ValidationStrategy):
    def validate(self, order: dict):
        if order["currency"] not in ["TWD", "USD"]:
            raise ValidationError(400, "Currency format is wrong")
