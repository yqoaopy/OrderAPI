import pytest
from order.order_converter import OrderConverter
from order.covert_strategies import USDToTWDConversionStrategy, NoConversionStrategy

def create_order(price_value="1000", currency="TWD"):
    return {
        "id": "A0000001",
        "name": "Leo",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": price_value,
        "currency": currency
    }

# check convert price
@pytest.mark.parametrize("price_value, currency, expected", [
    ("1000", "TWD", "1000"),
    ("1000", "USD", "31000"),
    ("1100", "TWD", "1100"),
])
def test_convert_price(price_value, currency, expected):
    order = create_order(price_value, currency)
    # 根據幣值選擇 策略
    if currency == "USD":
        converter = OrderConverter(USDToTWDConversionStrategy())
    else:
        converter = OrderConverter(NoConversionStrategy())
    result = converter.convert(order)
    assert result["price"] == expected
if __name__ == '__main__':
    pytest.main()
