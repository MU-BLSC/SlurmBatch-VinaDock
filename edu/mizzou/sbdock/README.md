# Slurm Batch Vina Docking


## What is it?

The Slurm Batch Vina Docking library is designed to optimize docking Vina in clusters managed by Slurm Workflow Manager. This library uses Slurm Workflow Manager and python programs to streamline the process of docking. This accepts only the ligand library and receptor as inputs, this library uses its 4 core modules to output the Vina scores, output pdbqt files, and top 100 ligands in various file formats. The parellelization using sbatch allows for many hundreds of thousands of ligands to be docked per hour depending on the scale of your cluster. 


## Installation and getting started

If you are working in Python and using conda (our recommendation), installation is super easy:

```shell-session
$ conda install sbdock
```
## Documentation

Available on the github page and in comments in the python files containing the modules. Detailed development information can be found in [development.md](../../development.md).

## Running Tests

To ensure the library is working correctly, you can run the unit tests using `pytest`.

1. **Install pytest:**
   ```bash
   pip install pytest
   ```

2. **Execute tests from the project root:**
   ```bash
   export PYTHONPATH="{pwd}/edu/mizzou/sbdock:$PYTHONPATH"
   pytest tests/
   ```

### Generate Config file

Once the vina docking values are 
