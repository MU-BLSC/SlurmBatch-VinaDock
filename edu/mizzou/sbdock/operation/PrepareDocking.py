#
#  Copyright (C) 2024-2025 University of Missouri, Bond Life Sciences Center, Dr.Kamal Singh, Ragavishagan Rajasekar
#
#   @@ All Rights Reserved @@
#  This file is part of the Sbdock Project - PrepareDocking.
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

class PrepareDocking:
    def __init__(self, config_file_path, ligands_csv_file_path, vina_exec_file_path, ligands_per_batch):
        """ sets the constructor variable values
            **Arguments**
              -config_file_path: The path to the config file with additional information for executing Vina. See GenerateConfig module.
              -ligands_csv_file_path: This is the .csv file in the format "unique_id", "smiles" that contains the name and smiles of all the ligands. See FilterMolecules module.
              -vina_exec_file_path: File path to the vina executable.
              -ligands_per_batch: number of ligands per batch that is executed in parallel
            **Returns**
              -lidir: Directory containing all the protonated 3D ligands in .pdbqt format
              -shelldir: Directory containing all the .sh files that have the command to execute vina
              -sbatchrun.sh : a .sh file that, when executed, will queue all the shell files in shelldir to the slurm workflow manager.
        """
        self.config_file_path = config_file_path
        self.ligands_csv_file_path = ligands_csv_file_path
        self.vina_exec_file_path = vina_exec_file_path
        self.ligands_per_batch = ligands_per_batch


    def prepare_docking(self):

        try:
            smiles_df = pd.read_csv(self.ligands_csv_file_path)

        except FileNotFoundError:
            print("Error: ligand csv file not found.")
            sys.exit(1)

        os.mkdir("slurmout")
        os.mkdir("slurmerr")
        os.mkdir("ligdir")
        os.mkdir("shelldir")
        file = open("sbatchrun.txt", "a")
        file.write("#!/bin/bash" + '\n')
        file.close()
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

                if (index == 0):
                    file = open("cmd.txt", "a")
                    file.write("#!/bin/bash" + '\n')
                    file.write(
                        f"{self.vina_exec_file_path} --ligand " + f"{ligdir}" + " --config " + f"{self.config_file_path}" + '\n')
                    file.close()
                else:
                    if (index % self.ligands_per_batch == 0):
                        file = open(f"cmd.txt", "a")
                        file.write(
                            f"{self.vina_exec_file_path} --ligand " + f"{ligdir}" + " --config " + f"{self.config_file_path}" + '\n')
                        file.close()
                        os.rename("cmd.txt", f"{file_name}.sh")
                        subprocess.run(["chmod", "+x", f"{file_name}.sh"])
                        subprocess.run(
                            ["mv", f"{os.getcwd()}/{file_name}.sh", f"{os.getcwd()}/shelldir/{file_name}.sh"])
                        file = open("sbatchrun.txt", "a")
                        file.write(
                            "sbatch" + f" --time=1:00:00" + f" --mem=100M" + f" --cpus-per-task=8" + f" --job-name={unique_id}.%j" + f" --output=./slurmout/{unique_id}_out" + f" --error=./slurmerr/{unique_id}_err" + f' --wrap=\"./shelldir/{file_name}.sh\"' + '\n')
                        file.close()
                        file = open("cmd.txt", "a")
                        file.write("#!/bin/bash" + '\n')
                        file.close()

                    else:
                        file = open(f"cmd.txt", "a")
                        file.write(
                            f"{self.vina_exec_file_path} --ligand " + f"{ligdir}" + " --config " + f"{self.config_file_path}" + '\n')
                        file.close()

            except Exception as e:
                print(e)
        os.rename("sbatchrun.txt", "sbatchrun.sh")
        subprocess.run(["chmod", "+x", "sbatchrun.sh"])
        os.remove("cmd.txt")
