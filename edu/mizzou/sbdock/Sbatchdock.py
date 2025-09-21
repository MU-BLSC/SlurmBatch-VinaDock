#
#  Copyright (C) 2024-2025 University of Missouri, Bond Life Sciences Center, Dr.Kamal Singh, Ragavishagan Rajasekar
#
#   @@ All Rights Reserved @@
#  This file is part of the Sbdock Project.
#  The contents are covered by the terms of the BSD license
#  which is included in the file license.txt, found at the root
#  of the Sbdock source tree.
#

from operation.SmilesTo3dSDF import SmilesTo3dSDF
from operation.SmilesToPDBQT import SmilesToPDBQT
from operation.GenerateConfig import GenerateConfig
from operation.PrepareDocking import PrepareDocking
from operation.ProcessPdbqtOutput import ProecessPdbqtOutput
from operation.FilterMolecules import FilterMolecules


class Sbatchdock():
    def __init__(self):
        pass

    def generateConfig(self, config_file_path, receptor_file_path, center_x, center_y, center_z, size_x, size_y, size_z, cpu):
        generateConfig = GenerateConfig(config_file_path, receptor_file_path, center_x, center_y, center_z, size_x, size_y, size_z, cpu)
        generateConfig.generate_config()

    def filterMolecules(self, unfiltered_smi_file_path, ligands_csv_file_path):
        filterMolecules = FilterMolecules( unfiltered_smi_file_path, ligands_csv_file_path)
        filterMolecules.filterSmilesToCSV()

    def prepareDocking(self, config_file_path, ligands_csv_file_path, vina_exec_file_path, ligands_per_batch):
        prepareDocking = PrepareDocking(config_file_path, ligands_csv_file_path, vina_exec_file_path, ligands_per_batch)
        prepareDocking.prepare_docking()

    def processPdbqtOutput(self, pdbqt_output_directory, ligands_csv_file_path):
        processPdbqtOutput = ProecessPdbqtOutput(pdbqt_output_directory, ligands_csv_file_path)
        processPdbqtOutput.process_pdbqt_output()

    def convertCSVSmilesToPDBQT(self,ligands_csv_file_path):
        smilesToPDBQT = SmilesToPDBQT(ligands_csv_file_path)
        smilesToPDBQT.convert_csv_smiles_to_pdbqt()

    def convertSmilesTo3dSDF(self,smiles_file_path,sdf_file_path):
        smilesTo3dSDF = SmilesTo3dSDF(smiles_file_path, sdf_file_path)
        smilesTo3dSDF.convert_smiles_to_3d_SDF()
