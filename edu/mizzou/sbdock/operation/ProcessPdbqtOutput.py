#
#  Copyright (C) 2024-2025 University of Missouri, Bond Life Sciences Center, Dr.Kamal Singh, Ragavishagan Rajasekar
#
#   @@ All Rights Reserved @@
#  This file is part of the Sbdock Project - ProecessPdbqtOutput.
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
from edu.mizzou.sbdock.operation.SmilesTo3dSDF import SmilesTo3dSDF

class ProecessPdbqtOutput:
    def __init__(self, pdbqt_output_directory, ligands_csv_file_path):
        """ sets the constructor variable values
            **Arguments**
                -pdbqt_output_directory: The directory containing all the _out.pdbqt output files from Vina
                -ligands_csv_file_path: his is the .csv file in the format "unique_id", "smiles" that contains the name and smiles of all the original ligands. See PrepareDocking module.
            **Returns**
                -output.csv: The .csv file in the format "unique_id", "vina_score"
                -sortedoutput.csv: The .csv file in the format "unique_id", "vina_score" but is sorted from the smallest vina score to the largest vina score
                -top100.smi: The smiles file containing all the top 100 smiles ranked based on "vina_score"
                -top100.sdf: The sdf file containing all the top 100 3D sdf structures ranked based on "vina_score"
        """
        self.pdbqt_output_directory = pdbqt_output_directory
        self.ligands_csv_file_path = ligands_csv_file_path

    def extract_vina_score(self, input_string):
        hyphen_index = input_string.find('-')
        if hyphen_index != -1:
            start_index = hyphen_index
            end_index = start_index + 5
            if len(input_string) >= end_index:
                return input_string[start_index:end_index].strip()
        return ""

    def smiles_to_sdf(self, smiles_file_path, sdf_file_path):
        """
        Converts a SMILES file to an SDF file.

        Args:
            smiles_file (str): Path to the input SMILES file.
            sdf_file (str): Path to the output SDF file.
        """
        smilesTo3dSDF = SmilesTo3dSDF(smiles_file_path, sdf_file_path)
        smilesTo3dSDF.convert_smiles_to_3d_SDF()

    def process_pdbqt_output(self):
        output_csv = 'output.csv'
        with open(output_csv, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['unique_id', 'vina_score'])  # Write header

            for filename in os.listdir(self.pdbqt_output_directory):
                if filename.endswith('out.pdbqt'):
                    filepath = os.path.join(self.pdbqt_output_directory, filename)
                    try:
                        with open(filepath, 'r') as file:
                            lines = file.readlines()
                            if len(lines) > 1:
                                second_line = lines[1].strip()
                                vina_score = self.extract_vina_score(second_line)
                            else:
                                second_line = "File does not have a second line"
                                vina_score = 0
                        csv_writer.writerow([filename.split(".")[1].removesuffix("_out"), vina_score])
                    except Exception as e:
                        csv_writer.writerow([filename, f"Error reading file: {e}"])
        unsortedout_df = pd.read_csv(output_csv, sep=',', header='infer')
        sortedout_df = unsortedout_df.sort_values(by='vina_score', ascending=True)
        sortedout_df.to_csv('sortedoutput.csv', index=False)
        top_100 = sortedout_df.head(100)
        ligands_df = pd.read_csv(self.ligands_csv_file_path, sep=',', header='infer')
        ligands_with_smiles_df = pd.merge(top_100, ligands_df, left_on='unique_id', right_on='unique_id', how='left')
        ligands_with_smiles_df[['smiles', 'unique_id']].to_csv('top100.smi', sep='\t', index=False)
        self.smiles_to_sdf("top100.smi", "top100.sdf")

        print(f"Data written to output.csv and sortedoutput.csv")
        print("top 100 written to top100.smi and top100.sdf")
