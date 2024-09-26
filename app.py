from flask import Flask, request, jsonify
from order.order_validator import OrderValidator, ValidationError
from order.order_converter import OrderConverter

app = Flask(__name__)

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:

        data = request.get_json()

        validator = OrderValidator()
        is_valid = validator.validate(data)
        if is_valid:
            converter = OrderConverter()
            data = converter.convert(data)
         
    except ValidationError as e:
        return jsonify({'error': str(e.message)}), e.status_code  
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500  

    return jsonify(data), 200  # 返回成功狀態碼

if __name__ == '__main__':
    app.run()