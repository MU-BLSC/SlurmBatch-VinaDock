#
#  Copyright (C) 2024-2025 University of Missouri, Bond Life Sciences Center, Dr.Kamal Singh, Ragavishagan Rajasekar
#
#   @@ All Rights Reserved @@
#  This file is part of the Sbdock Project - FilterMolecules.
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
from rdkit.Chem import Crippen
from rdkit.Chem import Lipinski
from rdkit.Chem import MolSurf
import meeko
import sys
import subprocess
import os
import csv

class FilterMolecules:
    def __init__(self, unfiltered_smi_file_path, ligands_csv_file_path):
        """
            **Arguments**

                - unfiltered_smi_file_path: This is the .smi file that contains a library of compounds in the smiles format.


            **Returns**
                - ligands_csv_file_path: This is the .csv file in the format "unique_id", "smiles" that contains the name and smiles of all the compounds
                    from the input library that passed this filter that checks for certain physical, chemical, and bioactivity parameters.
        """
        self.unfiltered_smi_file_path = unfiltered_smi_file_path
        self.ligands_csv_file_path = ligands_csv_file_path

    def filterSmilesToCSV(self):
        approved_2d_smi_data = []
        with open(self.unfiltered_smi_file_path, 'r') as file:
            for i, line in enumerate(file):
                tokens = line.split(" ")
                smi, unique_id = tokens[0], tokens[1].strip()
                mol = Chem.MolFromSmiles(smi)
                mw = Descriptors.ExactMolWt(mol)
                if 160 < mw < 480:
                    logp = Crippen.MolLogP(mol)
                    if -0.4 < logp < 2.5:
                        hbd = Lipinski.NumHDonors(mol)
                        if 0 <= hbd <= 5:
                            numatmh = mol.GetNumAtoms(onlyExplicit=False)
                            if 20 <= numatmh <= 70:
                                mr = Crippen.MolMR(mol)
                                if 40 <= mr <= 130:
                                    nr = Lipinski.NumRotatableBonds(mol)
                                    if 0 <= nr <= 10:
                                        tpsa = MolSurf.TPSA(mol, includeHs=1)
                                        if 0 <= tpsa <= 140:
                                            mc = Chem.GetFormalCharge(mol)
                                            if -2 <= mc <= 2:
                                                print(f"{unique_id} passed")
                                                approved_2d_smi_data.append([unique_id, smi])
                                            else:
                                                print(f"{unique_id} failed charge")
                                        else:
                                            print(f"{unique_id} failed tpsa")
                                    else:
                                        print(f"{unique_id} failed rotations")
                                else:
                                    print(f"{unique_id} failed molecular refractivity")
                            else:
                                print(f"{unique_id} failed atms")
                        else:
                            print(f"{unique_id} failed hbd")
                    else:
                        print(f"{unique_id} failed logp")
                else:
                    print(f"{unique_id} failed molecular weight")
        # field names
        fields = ['unique_id', 'smiles']
        # writing to csv file
        with open(self.ligands_csv_file_path, 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            csvwriter.writerow(fields)
            # writing the data rows
            csvwriter.writerows(approved_2d_smi_data)
