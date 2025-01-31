STRATEGIES_CODE = {
    "broadcast": {
        "write": """\t\tfor(int i = 0; i < remotes.arrayLength; i++) {\n\t\t\tconnection.connect(remotes[i])\n\t\t\tconnection.make(r)\n\t\t}\n""",
        "read": """\t\tconnection.connect(remotes[0])\n\t\treturn connection.make(r, responseBodyType)\n"""
    }
}

class StrategyGenerator():
    def __init__(self, strategies):
        self.strategies = strategies

    def provide_strategy(self, file):
        for strategy in self.strategies:
            if strategy in STRATEGIES_CODE:
                write_strategy_method_name = "{}Write".format(strategy)
                read_strategy_method_name = "{}Read".format(strategy)

                #write writeStrategy
                file.write("\tvoid {}(Request r) ".format(write_strategy_method_name) + "{\n")
                file.write(STRATEGIES_CODE[strategy]["write"])
                file.write("\t}\n")

                file.write("\n")

                # write readStrategy
                file.write("\tResponse {}(Request r, Type responseBodyType) ".format(read_strategy_method_name) + "{\n")
                file.write(STRATEGIES_CODE[strategy]["read"])
                file.write("\t}\n")

                file.write("\n")

        
        file.write("}\n") # finish iplementation
 