
class AdaptationGenerator:
    def __init__(self):
        pass

    def provide_daptation(self, file):
        self.provide_on_active(file)
        file.write("\n")
        self.provide_on_inactive(file)
    
    def provide_on_active(self, file):
        file.write("\tvoid AdaptEvents:active() {\n")
        file.write("\t}\n")
    
    def provide_on_inactive(self, file):
        file.write("\tvoid AdaptEvents:inactive() {\n")
        file.write("\t}\n")