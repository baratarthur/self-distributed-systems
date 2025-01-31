
class HeaderGenerator:
    def __init__(self, interface_file_path, dependencies, remotes):
        self.name = self.get_component_name(interface_file_path)
        self.general_dependencies = self.provide_general_dependecies(dependencies)
        self.component_dependencies = self.provide_component_dependecies(dependencies)
        self.remotes = remotes

    def get_component_name(self, interface_file_path) -> str:
        return interface_file_path.replace("resources/", "").replace(".dn", "").replace("/", ".")

    def provide_component_header(self, file):
        file.write(self.general_dependencies)
        file.write("\n")
        file.write(f"component provides {self.name} {self.get_component_definition()}" + " {\n")
        file.write(self.provide_component_resources())

    def get_component_definition(self) -> str:
        if self.component_dependencies != "":
            return "requires " + self.component_dependencies[:-2] # retirar ultima ", " adicional
        else:
            return ""
    
    def provide_general_dependecies(self, dependencies) -> str:
        return "".join([f"uses {dep['lib']}\n" for dep in dependencies if dep['alias'] == None])
    
    def provide_component_dependecies(self, dependencies) -> str:
        return "".join([f"{dep['lib']} {dep['alias']}, " for dep in dependencies if dep['alias'] != None])
    
    def provide_component_resources(self):
        resources = ""
        resources += self.provide_addressess()
        return resources
    
    def provide_addressess(self) -> str:
        var_assign = "\tAddress remotes[] = new Address[]("
        for remote in self.remotes:
            var_assign += f"new Address(\"{remote['address']}\", {remote['port']}),"
        var_assign = var_assign[:-1]
        var_assign += ")\n"
        return var_assign
    
    def get_interface_name(self) -> str:
        return self.name.split('.')[1]
