class ConversionStrategy:
    def convert(self, order: dict) -> dict:
        raise NotImplementedError("Subclasses should implement this method")


class USDToTWDConversionStrategy(ConversionStrategy):
    def convert(self, order: dict) -> dict:
        if order["currency"] == "USD":
            order["price"] = str(int(order["price"]) * 31)
            order["currency"] = "TWD"
        return order

# RMB to TWD
# class RMBToTWDConversionStrategy(ConversionStrategy):
#     def convert(self, order: dict) -> dict:
#         if order["currency"] == "RMB":
#             order["price"] = str(int(order["price"]) * 6)
#             order["currency"] = "TWD"
#         return order


class NoConversionStrategy(ConversionStrategy):
    def convert(self, order: dict) -> dict:
        return order
