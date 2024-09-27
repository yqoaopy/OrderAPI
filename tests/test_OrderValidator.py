import pytest
from order.order_validator import OrderValidator, ValidationError
from order.val_strategies import OrderFieldValidationStrategy, NameValidationStrategy, PriceValidationStrategy, CurrencyValidationStrategy

def create_order(name_value="Leo", price_value="1000", currency="TWD"):
    return {
        "id": "A0000001",
        "name": name_value,
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": price_value,
        "currency": currency
    }



@pytest.mark.parametrize("missing_field", [
    "name",
    "id",
    "address",
    "price",
    "currency",
])
def test_validate_required_fields(missing_field):
    strategies = [OrderFieldValidationStrategy()]
    validator = OrderValidator(strategies)
    order = create_order()

    # 刪除缺少的欄位
    order.pop(missing_field)

    with pytest.raises(ValidationError) as exc_info:
        validator.validate(order)

    assert exc_info.value.status_code == 400
    assert exc_info.value.message == f'Missing field: {missing_field}'

@pytest.mark.parametrize("field, invalid_value", [
    ("id", 123),            # id 應為字串，但提供了整數
    ("name", 456),          # name 應為字串，但提供了整數
    ("currency", 789),      # currency 應為字串，但提供了整數
])
def test_validate_value_type(field, invalid_value):
    strategies = [OrderFieldValidationStrategy()]
    validator = OrderValidator(strategies)
    order = create_order()

    # 修改無效的欄位值
    order[field] = invalid_value

    with pytest.raises(ValidationError) as exc_info:
        validator.validate(order)

    assert exc_info.value.status_code == 400
    assert exc_info.value.message == f"{field.capitalize()} must be a string."

# check validate success
@pytest.mark.parametrize("name_value, price_value, currency", [
    ("Melody", "1000", "TWD"),
    ("Melody", "1000", "USD"),
    ("Melody", "2000", "TWD"),
])
def test_validate_success(name_value, price_value, currency):
    strategies = [OrderFieldValidationStrategy(), NameValidationStrategy(), PriceValidationStrategy(), CurrencyValidationStrategy()]
    validator = OrderValidator(strategies)
    order = create_order(name_value, price_value, currency)
    assert validator.validate(order) == True    

# name contains non-English char
def test_validate_name_invalid():
    strategies = [NameValidationStrategy()]
    validator = OrderValidator(strategies)
    order = create_order(name_value="Melody GG")

    with pytest.raises(ValidationError) as exc_info:
        validator.validate(order)
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == 'Name contains non-English characters'

# name first char is not upper
def test_validate_name_first_char_invalid():
    strategies = [NameValidationStrategy()]
    validator = OrderValidator(strategies)
    order = create_order(name_value="melody")
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(order)
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == 'Name is not capitalized'

# price more than 2000
def test_validate_price_invalid():
    strategies = [PriceValidationStrategy()]
    validator = OrderValidator(strategies)
    order = create_order(price_value=5000)
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(order)
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == 'Price is over 2000'

# currency is not (TWD or USD)
def test_validate_currency_invalid():
    strategies = [CurrencyValidationStrategy()]
    validator = OrderValidator(strategies)
    order = create_order(currency="RMB")
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(order)
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == 'Currency format is wrong'


if __name__ == '__main__':
    pytest.main()
