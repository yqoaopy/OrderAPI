class ValidationError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        
class OrderValidator:
    def validate(self, order: dict) -> bool:
          
        # check filed "name" contains non-English characters
        if not order["name"].isalpha():
            raise ValidationError(400, f"Name contains non-English characters")
        
        # check filed "name" first letter not capitalized
        if not order["name"][0].isupper():
            raise ValidationError(400, f"Name is not capitalized")

        # check filed "price" > 2000
        if int(order["price"]) > 2000:
            raise ValidationError(400, f"Price is over 2000")
        
        # check filed "currency" is "TWD" or "USD"
        if order["currency"] not in ["TWD", "USD"]:
            raise ValidationError(400, f"Currency format is wrong")
        
        return True