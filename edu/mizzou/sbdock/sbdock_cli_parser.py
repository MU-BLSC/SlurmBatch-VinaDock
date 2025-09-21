#
#  Copyright (C) 2024-2025 University of Missouri, Bond Life Sciences Center, Dr.Kamal Singh, RagaVishagan Rajasekar
#
#   @@ All Rights Reserved @@
#  This file is part of the Sbdock Project.
#  The contents are covered by the terms of the BSD license
#  which is included in the file license.txt, found at the root
#  of the Sbdock source tree.
#

import json
import argparse
from enum import Enum
from Sbatchdock import Sbatchdock

class ValidateAndInvoke():
    def __init__(self,function_name, json_dict):
        self.function_name = function_name
        self.json_dict = json_dict
        self.sbdock = Sbatchdock()

    def _validate_input_data(self):
        print(f"self.function_name {self.function_name}")
        match self.function_name:
            case "generateConfig":
                if "config_file_path" not in self.json_dict:
                    raise ValueError("Input value config_file_path is required and cannot be empty.")
                if "receptor_file_path" not in self.json_dict:
                    raise ValueError("Input value receptor_file_path is required and cannot be empty.")
                if "center_x" not in self.json_dict:
                    raise ValueError("Input value center_x is required and cannot be empty.")
                if "center_y" not in self.json_dict:
                    raise ValueError("Input value center_y is required and cannot be empty.")
                if "center_z" not in self.json_dict:
                    raise ValueError("Input value center_z is required and cannot be empty.")
                if "size_x" not in self.json_dict:
                    raise ValueError("Input value size_x is required and cannot be empty.")
                if "size_y" not in self.json_dict:
                    raise ValueError("Input value size_y is required and cannot be empty.")
                if "size_z" not in self.json_dict:
                    raise ValueError("Input value size_z is required and cannot be empty.")
                if "cpu" not in self.json_dict:
                    raise ValueError("Input value cpu is required and cannot be empty.")
            case "filterMolecules":
                if "unfiltered_smi_file_path" not in self.json_dict:
                    raise ValueError("Input value unfiltered_smi_file_path is required and cannot be empty.")
                if "ligands_csv_file_path" not in self.json_dict:
                    raise ValueError("Input value ligands_csv_file_path is required and cannot be empty.")
            case "prepareDocking":
                if "ligands_csv_file_path" not in self.json_dict:
                    raise ValueError("Input value ligands_csv_file_path is required and cannot be empty.")
                if "config_file_path" not in self.json_dict:
                    raise ValueError("Input value config_file_path is required and cannot be empty.")
                if "vina_exec_file_path" not in self.json_dict:
                    raise ValueError("Input value vina_exec_file_path is required and cannot be empty.")
                if "ligands_per_batch" not in self.json_dict:
                    raise ValueError("Input value ligands_per_batch is required and cannot be empty.")
            case "processPdbqtOutput":
                if "pdbqt_output_directory" not in self.json_dict:
                    raise ValueError("Input value pdbqt_output_directory is required and cannot be empty.")
            case "convertCSVSmilesToPDBQT":
                if "ligands_csv_file_path" not in self.json_dict:
                    raise ValueError("Input value ligands_csv_file_path is required and cannot be empty.")
            case "convertSmilesTo3dSDF":
                if "smiles_file_path" not in self.json_dict:
                    raise ValueError("Input value smiles_file_path is required and cannot be empty.")
                if "sdf_file_path" not in self.json_dict:
                    raise ValueError("Input value sdf_file_path is required and cannot be empty.")
            case _:  # Default case, similar to 'default' in switch
                print("Input Function name does not match any specific case")

    def _invoke_function(self):
        print(f"self.function_name {self.function_name}")
        match self.function_name:
            case "generateConfig":
                self.sbdock.generateConfig(config_file_path=self.json_dict["config_file_path"], receptor_file_path=self.json_dict["receptor_file_path"], center_x=self.json_dict["center_x"], center_y=self.json_dict["center_y"], center_z=self.json_dict["center_z"], size_x=self.json_dict["size_x"], size_y=self.json_dict["size_y"], size_z=self.json_dict["size_z"], cpu=self.json_dict["cpu"])
            case "filterMolecules":
                self.sbdock.filterMolecules(unfiltered_smi_file_path=self.json_dict["unfiltered_smi_file_path"], ligands_csv_file_path=self.json_dict["ligands_csv_file_path"])
            case "prepareDocking":
                self.sbdock.prepareDocking(config_file_path=self.json_dict["config_file_path"], ligands_csv_file_path=self.json_dict["ligands_csv_file_path"], vina_exec_file_path=self.json_dict["vina_exec_file_path"], ligands_per_batch=self.json_dict["ligands_per_batch"])
            case "processPdbqtOutput":
                self.sbdock.processPdbqtOutput(pdbqt_output_directory=self.json_dict["pdbqt_output_directory"], ligands_csv_file_path=self.json_dict["ligands_csv_file_path"])
            case "convertCSVSmilesToPDBQT":
                self.sbdock.convertCSVSmilesToPDBQT(ligands_csv_file_path=self.json_dict["ligands_csv_file_path"])
            case "convertSmilesTo3dSDF":
                self.sbdock.convertSmilesTo3dSDF(smiles_file_path=self.json_dict["smiles_file_path"],sdf_file_path=self.json_dict["sdf_file_path"])
            case _:  # Default case, similar to 'default' in switch
                print("Input Function name does not match any specific case")

    def validate_input_and_invoke_functions(self):
        self._validate_input_data()
        self._invoke_function()

class FunctionNames(str, Enum):
    gen_config = 'generateConfig'
    filter = 'filterMolecules'
    preo_docking = 'prepareDocking'
    proc_pdbqt_file = 'processPdbqtOutput'
    convert_csv_smiles_to_pdbqt = 'convertCSVSmilesToPDBQT'
    convert_smiles_to_3d_sdf = 'convertSmilesTo3dSDF'

    def __str__(self):
        return self.value

def main():
    """
    This function contains the main logic of the program.
    """
    json_content = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--function_name",  required=True, type=FunctionNames, choices=[function_name.value for function_name in FunctionNames])
    parser.add_argument("-jf", "--json_file_name", required=False, type=str)
    parser.add_argument("-js", "--json_file_string", required=False, type=str)
    args = parser.parse_args()
    function_name = args.function_name

    if (args.json_file_name):
        with open(args.json_file_name) as json_data:
            json_content = json.load(json_data)
            print(json_content)
    elif (args.json_file_string):
        json_content = json.loads(args.json_file_string)
        print(json_content)
    else:
        print("throw an exception stating json string or json file_name is required")
        raise ValueError("Input value json_string OR json_file is required and cannot be empty.")

    validateAndInvoke = ValidateAndInvoke(function_name,json_content)
    validateAndInvoke.validate_input_and_invoke_functions()

if __name__ == "__main__":
    main()
