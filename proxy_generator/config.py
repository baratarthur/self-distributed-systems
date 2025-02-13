import json

class DpdlReader:
    def __init__(self, json_path):
        config_json = json.load(json_path)
        self.output_folder = config_json['output_folder']
        self.remotes = config_json['remotes']
        self.dependencies = config_json['dependencies']
        self.attributes = config_json['attributes']
        self.methods = config_json['methods']
        self.on_active = config_json['onActive']
        self.on_inactive = config_json['onInactive']
