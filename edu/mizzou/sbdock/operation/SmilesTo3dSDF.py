#
#  Copyright (C) 2024-2025 University of Missouri, Bond Life Sciences Center, Dr.Kamal Singh, Ragavishagan Rajasekar
#
#   @@ All Rights Reserved @@
#  This file is part of the Sbdock Project - SmilesTo3dSDF.
#  The contents are covered by the terms of the BSD license
#  which is included in the file license.txt, found at the root
#  of the Sbdock source tree.
#

import json
import argparse
from enum import Enum
import pandas as pd
from rdkit.Chem import AllChem
from rdkit import Chem
import meeko
import sys
import subprocess
import os

class SmilesTo3dSDF:
    def __init__(self,smiles_file_path,sdf_file_path):
        """ sets the constructor variable values
            **Arguments**
              - smiles_file_path: This is the .smi file containing all the smiles molecules that will be converted to 3D sdf.
            **Returns**
              - sdf_file_path: This is the .sdf file containing all the 3d conformers of the aforementioned smiles molecules.
              None:

        """
        self.smiles_file_path=smiles_file_path
        self.sdf_file_path=sdf_file_path

    def convert_smiles_to_3d_SDF(self):
        with open(self.smiles_file_path, 'r') as f_in, Chem.SDWriter(self.sdf_file_path) as writer:
            for line in f_in:
                smiles = line.strip()
                try:
                    mol = Chem.MolFromSmiles(smiles)
                    mol = Chem.AddHs(mol)
                except Exception as e:
                    print(f"{e}")
                try:
                    AllChem.EmbedMolecule(mol, AllChem.ETKDGv2())  # Use ETKDGv2 for better conformer generation
                    AllChem.MMFFOptimizeMolecule(mol)  # Optimize the generated conformer using MMFF94 force field
                except Exception as e:
                    print(f"Error generating 3D coordinates or optimizing for SMILES '{smiles}': {e}")
                    continue
                if mol is not None:  # Handle cases where SMILES is invalid
                    writer.write(mol)
