from order.order_validator import ValidationError


class ValidationStrategy:
    def validate(self, order: dict):
        raise NotImplementedError("Subclasses should implement this method")


# check all item and value type is str address is dict 
class OrderFieldValidationStrategy(ValidationStrategy):
    def validate(self, order: dict):
        required_fields = ['id', 'name', 'address', 'price', 'currency']
        # 檢查所有必需的欄位是否存在且為字串，address 應為字典
        for field in required_fields:
            if field not in order:
                raise ValidationError(400, f"Missing field: {field}")
            if field == "address":
                if not isinstance(order[field], dict):
                    raise ValidationError(400, "Address must be a dictionary.")
                 # 檢查 address 下的子欄位
                address_fields = ['city', 'district', 'street']
                for address_field in address_fields:
                    if address_field not in order[field]:
                        raise ValidationError(400, f"Missing address field: {address_field}")
                    if not isinstance(order[field][address_field], str):
                        raise ValidationError(400, f"{address_field.capitalize()} must be a string.")
            elif not isinstance(order[field], str):
                raise ValidationError(400, f"{field.capitalize()} must be a string.")

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
