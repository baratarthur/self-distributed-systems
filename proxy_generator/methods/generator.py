RETURN_TYPES = {
    "VOID": "void",
    "STR": "String",
    "INT": "int",
    "CHAR": "char"
}

class MethodsGenerator:
    def __init__(self, methods, interface_name, attributes):
        self.methods = methods
        self.interface_name = interface_name
        self.attributes = attributes

    def provide_method_implementation(self, file):
        self.provide_methods(file)
        self.provide_metadata_factory(file)

    def provide_methods(self, file):
        for method in self.methods:
            method_props = self.methods[method]
            file.write(f"\t{method_props['returnType']} {self.interface_name}:{method} (")
            if 'arguments' in method_props:
                for i, arg in enumerate(method_props['arguments']):
                    arg_string = f"store {arg['type']} {arg['name']}" if 'store' in arg and arg['store'] else f"{arg['type']} {arg['name']}"
                    file.write(arg_string)
                    if i != len(method_props['arguments']) - 1: file.write(",")
            file.write(") {\n")

            # if has argument should distribute the argument
            # if method_props["operation"] == "write":
            if 'arguments' in method_props:
                for i, arg in enumerate(method_props['arguments']):
                    self.provide_metadata_for_write_method(file, i, method, arg['name'])
                    attribute_affected = self.attributes[arg["connectsTo"]]
                    operation_name = method_props["operation"].capitalize()
                    strategy_method_name = "{}{}".format(attribute_affected["strategy"], operation_name)
                    file.write("\t\t")
                    self.provide_strategy_call_for_order(file, i, strategy_method_name)
            else:
                self.provide_metadata_for_read_method(file, i, method)
                attribute_affected = self.attributes[method_props["connectsTo"]]
                operation_name = method_props["operation"].capitalize()
                strategy_method_name = "{}{}".format(attribute_affected["strategy"], operation_name)
                if method_props['returnType'] != RETURN_TYPES["VOID"]: file.write("\t\tResponse res = ")
                else: file.write("\t\t")
                self.provide_strategy_call_for_order(file, i, strategy_method_name, method_props["returnType"])
                if method_props['returnType'] != RETURN_TYPES["VOID"]: file.write("\t\treturn res.d\n") # verificar se funciona
                #todo: adicionar conversão de dado do response para tipo de saída da função e retornar o dado

            file.write("\t}\n")
            file.write("\n")

    def provide_metadata_for_write_method(self, file, order, method_name, arg_name):
        file.write("\t\tRequest req{} = new Request(buildMetaForMethod(\"{}\"), {})\n".format(order, method_name, arg_name))
    
    def provide_metadata_for_read_method(self, file, order, method_name):
        file.write("\t\tRequest req{} = new Request(buildMetaForMethod(\"{}\"))\n".format(order, method_name))
    
    def provide_strategy_call_for_order(self, file, order, strategy, returnType=None):
        if returnType is None or returnType == RETURN_TYPES["VOID"]: file.write("{}(req{})\n".format(strategy, order))
        else: file.write("{}(req{}, typeof({}))\n".format(strategy, order, returnType))

    def provide_metadata_factory(self, file):
        file.write("""\tMetadata[] buildMetaForMethod(char method[]) {\n\t\tMetadata metaMethod = new Metadata("method", method)\n\t\treturn new Metadata[](metaMethod)\n\t}\n""")
