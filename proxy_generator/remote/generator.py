from helpers.write_component_helper import WriteComponentHelper

replicated_strategies = ['distribute']

class RemoteGenerator:
    def __init__(self, file, component_name, component_package,
                 component_methods, connection_library="network.rpc.RPCUtil rpc"):
        self.writer = WriteComponentHelper(file)
        self.component_name = component_name
        self.component_package = component_package
        self.component_methods = component_methods
        self.resources = [
            "net.TCPSocket",
            "net.TCPServerSocket",
            "io.Output out",
            "data.IntUtil iu",
            "data.json.JSONEncoder je",
            "data.StringUtil su",
            connection_library,
            f"{component_package}.{component_name.capitalize()} remoteComponent",
        ]
    
    def provide_header(self):
        self.writer.write_idented("uses Constants")
        self.writer.break_line()
        self.writer.write_idented('const char debugMSG[] = "[@Remote]"')
        self.writer.break_line()
        self.writer.break_line()

    def provide_component_resources(self):
        return "requires " + ", ".join(self.resources)

    def provide_server_methods(self):
        self.writer.write_idented("bool serviceStatus = false")
        inside_component = self.writer.use_idented_flow(f"component provides server.Remote:{self.component_name} {self.provide_component_resources()}")
        
        inside_component(self.writer, [
            "TCPServerSocket host = new TCPServerSocket()",
            "serviceStatus = true",
            "\n",
            self.provie_init_method(),
            self.provide_handle_request()
        ])

    def provie_init_method(self):
        return self.writer.provide_idented_flow("void Remote:start(int PORT)", [
            "TCPServerSocket host = new TCPServerSocket()",
            "serviceStatus = true",
            "\n",
            self.writer.provide_idented_flow("if (!host.bind(TCPServerSocket.ANY_ADDRESS, PORT))", [
                'out.println("Error: failed to bind master socket")',
                "return"
            ]),
            'out.println("$debugMSG - Server started on port $(iu.makeString(PORT))")',
            self.writer.provide_idented_flow("while (serviceStatus)", [
                "TCPSocket client = new TCPSocket()",
                "if (client.accept(host)) asynch::handleRequest(client)"
            ])
        ])

    def provide_handle_request(self):
        return self.writer.provide_idented_flow("void Remote:handleRequest(TCPSocket s)", [
            "char requestContent[] = rpc.receiveData(s)",
            "if(requestContent == null) s.disconnect()",
            "Request req = rpc.parseRequestFromString(requestContent)",
            "Response res = process(req)",
            "char rawResponse[] = rpc.buildRawResponse(res)",
            "s.send(rawResponse)",
            "s.disconnect()",
        ])

    def provide_processing_method(self):
        strategies_provider = [
            "char method[] = rpc.getMethodFromMetadata(req.meta)",
            "\n",
        ]

        for method in self.component_methods:
            method_configs = self.component_methods[method]
            # print(method_configs)
            if method_configs["strategy"] in replicated_strategies:
                parameters_format_type = f"{method[0].upper() + method[1:]}ParamsFormat"
                strategies_provider.append(
                    self.writer.provide_idented_flow(f'if(method == "{method}")',[
                        f"{parameters_format_type} paramsData = je.jsonToData(req.content, typeof({parameters_format_type}))",
                        f"{method_configs['returnType']} result = remoteComponent.{method}({self.provide_virables_for_method(method_configs)})",
                        f'return rpc.buildResponseWithData("{method}", "200", remoteComponent.{method_configs["remoteReturnParser"].format("result")})'
                    ])
                )
        strategies_provider.append('return rpc.buildResponse(method, "404")')

        processing_method = self.writer.use_idented_flow("Response process(Request req)")
        processing_method(self.writer, strategies_provider)

    def provide_virables_for_method(self, method_config) -> str:
        def get_formated_parser(param):
            return param['variableParser'].format(f"paramsData.{param['name']}")

        return ",".join([f"remoteComponent.{get_formated_parser(param)}" for param in method_config['parameters']])    
