class DistanceStrategy:

    def __init__(self, source, strategy=None):
        self.strategy = strategy
        self.source = source

    def set_strategy(self, obj):
        self.strategy = obj

    def get_strategy(self):
        return self.strategy

    def compute_distance(self, target):
        if self.strategy is None:
            raise NotImplementedError("Strategy is not defined")
        return self.strategy.compute_distance(self.source, target)

