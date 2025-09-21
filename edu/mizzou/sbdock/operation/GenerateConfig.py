#
#  Copyright (C) 2024-2025 University of Missouri, Bond Life Sciences Center, Dr.Kamal Singh, Ragavishagan Rajasekar
#
#   @@ All Rights Reserved @@
#  This file is part of the Sbdock Project - GenerateConfig.
#  The contents are covered by the terms of the BSD license
#  which is included in the file license.txt, found at the root
#  of the Sbdock source tree.
#

import json
import argparse
from enum import Enum
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
import meeko
import sys
import subprocess
import os
import csv


class GenerateConfig:
    def __init__(self, config_file_path, receptor_file_path, center_x, center_y, center_z, size_x, size_y, size_z, cpu):
        """
            **Arguments**
                The arguments are values and file paths that are needed in the execution of Vina
            **Returns**
                A Vina config file at config_file_path
        """
        self.config_file_path = config_file_path
        self.receptor_file_path = receptor_file_path
        self.center_x = center_x
        self.center_y = center_y
        self.center_z = center_z
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.cpu = cpu

    def generate_config(self):
        try:
            with open(self.config_file_path, "w") as file:
                file.write("receptor = " + f"{self.receptor_file_path}\n")
                file.write("center_x = " + f"{self.center_x}\n")
                file.write("center_y = " + f"{self.center_y}\n")
                file.write("center_z = " + f"{self.center_z}\n")
                file.write("size_x = " + f"{self.size_x}\n")
                file.write("size_y = " + f"{self.size_y}\n")
                file.write("size_z = " + f"{self.size_z}\n")
                file.write("cpu = " + f"{self.cpu}\n")
        except FileNotFoundError:
            print(f"Error: {self.config_file_path} file not found.")
            sys.exit(1)