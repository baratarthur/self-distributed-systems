import json

class DidlReader:
    def __init__(self, json_path):
        config_json = json.load(json_path)
        self.output_folder = config_json['outputFolder']
        self.component_file = config_json['componentFile']
        self.dependencies = config_json['dependencies']
        self.attributes = config_json['attributes']
        self.methods = config_json['methods']
        self.on_active = self.calculate_on_active()
        self.on_inactive = self.calculate_on_inactive()
    
    def calculate_on_active(self) -> list:
        # TODO: create a name system to generate remote pod names
        instructions = ['remotes = podCreator.createPods(2, "dana-remote")']
        for attribute in self.attributes:
            if 'calculateWith' in self.attributes[attribute]:
                instructions.append(f"{self.attributes[attribute]['calculateWith']}({attribute})")
            elif 'calculateWithEach' in self.attributes[attribute]:
                instructions.append(f"for(int i = 0; i < {attribute}.arrayLength; i++)" + "{")
                instructions.append(f"\t{self.attributes[attribute]['calculateWithEach']}({attribute}[i])")
                instructions.append("}")
        return instructions

    def calculate_on_inactive(self) -> list:
        instructions = []
        for attribute in self.attributes:
            instructions.append(f"{attribute} = get{attribute[0].upper() + attribute[1:]}()")
        instructions.append("podCreator.deleteAllPods(remotes)")
        return instructions
