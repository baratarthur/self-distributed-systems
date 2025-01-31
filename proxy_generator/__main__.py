import os
from config import DpdlReader
from header.generator import HeaderGenerator
from strategy.generator import StrategyGenerator
from methods.generator import MethodsGenerator

IDL_EXTENSION = "dpdl"

idl_resources = []

for (path, dirname, files) in os.walk("resources"):
    for file in files:
        file_extension_type = file.split(".")[-1]
        if file_extension_type != IDL_EXTENSION: continue
        idl_resources.append(path + "/" + file)

for dpdl_filepath in idl_resources:
    interface_filepath = dpdl_filepath.replace(".dpdl", ".dn")

    with open(dpdl_filepath, "r") as dpdl_file, open(interface_filepath, "r") as interface_file:
        dpdl_config = DpdlReader(dpdl_file)
        interface_file_text = interface_file.read().replace("\n", "")

        # verify if outputpath exists
        if not os.path.exists(dpdl_config.output_folder):
            os.makedirs(dpdl_config.output_folder)
        
        file_name = dpdl_filepath.split("/")[-1].replace(".dpdl", ".proxy.dn")
        output_file_path = f"{dpdl_config.output_folder}/{file_name}"

        strategies = [dpdl_config.attributes[attr]['strategy'] for attr in dpdl_config.attributes]

        ComponentHeader = HeaderGenerator(interface_filepath, dpdl_config.dependencies, dpdl_config.remotes)
        ComponentMethods = MethodsGenerator(dpdl_config.methods, ComponentHeader.get_interface_name(), dpdl_config.attributes)
        ComponentStrategyAndFooter = StrategyGenerator(strategies)

        with open(output_file_path, "w") as out_file:
            ComponentHeader.provide_component_header(out_file)
            out_file.write("\n")
            ComponentMethods.provide_method_implementation(out_file)
            out_file.write("\n")
            ComponentStrategyAndFooter.provide_strategy(out_file)
