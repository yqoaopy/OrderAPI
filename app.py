from flask import Flask, request, jsonify
from order.order_validator import OrderValidator, ValidationError
from order.val_strategies import OrderFieldValidationStrategy, NameValidationStrategy, PriceValidationStrategy, CurrencyValidationStrategy
from order.order_converter import OrderConverter
from order.covert_strategies import USDToTWDConversionStrategy,NoConversionStrategy
app = Flask(__name__)

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:

        data = request.get_json()

        Val_strategies = [
            OrderFieldValidationStrategy(),
            NameValidationStrategy(),
            CurrencyValidationStrategy()
        ]
        validator = OrderValidator(Val_strategies)
        is_valid = validator.validate(data)
        if is_valid:
            # 根據幣值決定採用何種轉換策略
            if data["currency"] == "USD":
                converter = OrderConverter(USDToTWDConversionStrategy())
            else:
                converter = OrderConverter(NoConversionStrategy())
            data = converter.convert(data)

            # 在轉換後進行價格驗證 base on TWD
            price_validator = PriceValidationStrategy()
            price_validator.validate(data)
            
         
    except ValidationError as e:
        return jsonify({'error': str(e.message)}), e.status_code  
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred."}), 500  

    return jsonify(data), 200  # 返回成功狀態碼

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)