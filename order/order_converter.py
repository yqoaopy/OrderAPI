class OrderConverter:
    def convert(self, order: dict) -> dict:
        # if filed "currency" is "USD" "price" x 31 and chage "currency" to "TWD"
        if order["currency"] == "USD":
            order["price"] = str(int(order["price"]) * 31)
            order["currency"] = "TWD"   
        
        return order

