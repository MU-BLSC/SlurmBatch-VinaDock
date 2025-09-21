#
#  Copyright (C) 2024-2025 University of Missouri, Bond Life Sciences Center, Dr.Kamal Singh, Ragavishagan Rajasekar
#
#   @@ All Rights Reserved @@
#  This file is part of the Sbdock Project - SmilesToPDBQT.
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

class SmilesToPDBQT:
    def __init__(self,ligands_csv_file_path):
        """ sets the constructor variable values
            **Arguments**
                -ligands_csv_file_path: This is the .csv file in the format "unique_id", "smiles" that contains the name and smiles of all the ligands. See FilterMolecules module.
            **Returns**
                -lidir: Directory containing all the protonated 3D ligands in .pdbqt format
              None:

        """
        self.ligands_csv_file_path=ligands_csv_file_path

    def convert_csv_smiles_to_pdbqt(self):
        os.mkdir("ligdir")
        try:
            smiles_df = pd.read_csv(self.ligands_csv_file_path)

        except FileNotFoundError:
            print("Error: ligand csv file not found.")
            sys.exit(1)
        for index, row in smiles_df.iterrows():
            smiles = row['smiles']  # Assuming 'smiles' is the column name in your CSV
            unique_id = row['unique_id']
            try:

                # Convert SMILES to RDKit molecule

                lig = Chem.MolFromSmiles(smiles)
                protonated_lig = Chem.AddHs(lig)
                AllChem.EmbedMolecule(protonated_lig)

                # Prepare ligand using Meeko

                meeko_prep = meeko.MoleculePreparation()
                meeko_prep.prepare(protonated_lig)
                lig_pdbqt = meeko_prep.write_pdbqt_string()
                # Write PDBQT to file
                file_name = f'{index}.{unique_id}'
                file = open(f"{file_name}.pdbqt", "w")
                file.write(lig_pdbqt)
                file.close()
                ligdir = f"{os.getcwd()}/ligdir/{file_name}.pdbqt"
                subprocess.run(["mv", f"{os.getcwd()}/{file_name}.pdbqt", f"{ligdir}"])
            except Exception as e:
                print(e)
