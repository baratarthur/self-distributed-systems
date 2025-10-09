import json

class DidlReader:
    def __init__(self, json_path):
        config_json = json.load(json_path)
        self.output_folder = config_json['outputFolder']
        self.component_file = config_json['componentFile']
        self.remotes = config_json['remotes']
        self.dependencies = config_json['dependencies']
        self.attributes = config_json['attributes']
        self.methods = config_json['methods']
        self.on_active = self.calculate_on_active(config_json)
        self.on_inactive = self.calculate_on_inactive(config_json)
    
    def calculate_on_active(self, json) -> list:
        instructions = []
        for attribute in json['attributes']:
            if 'calculateWith' in json['attributes'][attribute]:
                instructions.append(f"{json['attributes'][attribute]['calculateWith']}({attribute})")
            elif 'calculateWithEach' in json['attributes'][attribute]:
                instructions.append(f"for(int i = 0; i < {attribute}.arrayLength; i++)" + "{")
                instructions.append(f"\t{json['attributes'][attribute]['calculateWithEach']}({attribute}[i])")
                instructions.append("}")
        return instructions

    def calculate_on_inactive(self, json) -> list:
        instructions = []
        for attribute in json['attributes']:
            instructions.append(f"{attribute} = get{attribute[0].upper() + attribute[1:]}()")
        return instructions
