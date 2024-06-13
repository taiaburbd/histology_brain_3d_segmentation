#!/bin/bash

# exec bash
source /user1/ngmm/st6962co/.bashrc
# Print a message indicating the start of the script execution.
echo "Starting my shell script"

# Assign the path or name of the PyTorch module to a variable.
MY_PYTORCH_MODULE="pytorch/1.11.0/cuda/11.3.1/gpu"

# Assign the root directory path for the project to a variable.
MYROOTDIR="/work/shared/ngmm/scripts/Taiabur/ngmm-nnunet/"

# Load the PyTorch module using the module management system.
module load ${MY_PYTORCH_MODULE}

# Change the current working directory to the project root directory.
# If changing the directory fails (e.g., the directory does not exist), exit the script to avoid further errors.
# cd $MYROOTDIR || exit
cd $MYROOTDIR

# Activate a Conda environment named `env_tf`. 
# This prepares the shell with the environment's specific Python and library setup.
conda activate /user1/ngmm/st6962co/.conda/envs/env_ng

# Execute the nnUNet training command with specified parameters.
# This is likely a command specific to the nnUNet framework for medical image segmentation.

#the number after train corresponds to the training dataset - should be unique and refering to Dataset00X
# fold 1
nnUNetv2_train 4 3d_fullres 0 --npz 

# Print a message indicating the end of the script's execution.
echo "Ending the shell "
