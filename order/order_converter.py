class OrderConverter:
    def __init__(self, strategies):
        self.strategies = strategies

    def convert(self, order: dict)->dict: 
        data = self.strategies.convert(order)
        return data

