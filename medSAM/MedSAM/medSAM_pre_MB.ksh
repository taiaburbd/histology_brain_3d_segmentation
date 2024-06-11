#!/bin/bash

# Assign the path or name of the PyTorch module to a variable.
MY_PYTORCH_MODULE="pytorch/1.11.0/cuda/11.3.1/gpu"

# Assign the root directory path for the project to a variable.
MYROOTDIR="/work/shared/ngmm/scripts/Taiabur/medSAM/MedSAM/"

# module load ${MY_PYTHON_MODULE}
module load ${MY_PYTORCH_MODULE}

# cd $MYROOTDIR 
cd $MYROOTDIR

python pre_MB.py
 
# Print a message indicating the end of the script's execution.
echo "Ending the shell "