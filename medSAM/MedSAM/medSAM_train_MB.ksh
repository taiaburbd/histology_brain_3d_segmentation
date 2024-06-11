#!/bin/bash

# exec bash
source /user1/ngmm/tr855969/.bashrc

# Assign the path or name of the PyTorch module to a variable.
MY_PYTORCH_MODULE="pytorch/1.11.0/cuda/11.3.1/gpu"

# Assign the root directory path for the project to a variable.
MYROOTDIR="/work/shared/ngmm/scripts/Taiabur/medSAM/MedSAM/"

# This prepares the shell with the environment's specific Python and library setup.
conda activate /user1/ngmm/tr855969/.conda/envs/env_tf


# module load ${MY_PYTHON_MODULE}
module load ${MY_PYTORCH_MODULE}

# cd $MYROOTDIR 
cd $MYROOTDIR

python train_one_gpu_MB.py --tr_npy_path data/npy/MB_Nabd --device cuda:0

 
# Print a message indicating the end of the script's execution.
echo "Ending the shell "