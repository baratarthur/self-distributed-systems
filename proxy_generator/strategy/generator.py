
class StrategyGenerator():
    def __init__(self, strategies):
        self.strategy = strategies

    def provide_strategy(self, file):
        file.write("}")
