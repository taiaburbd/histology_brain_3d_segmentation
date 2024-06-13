#!/bin/bash

# exec bash
source /user1/ngmm/st6962co/.bashrc
# Print a message indicating the start of the script execution.
echo "Starting my shell script"

# Assign the path or name of the PyTorch module to a variable.
MY_PYTORCH_MODULE="pytorch/1.11.0/cuda/11.3.1/gpu"

# Assign the path or name of the Python module to a variable.
# MY_PYTHON_MODULE="python/3.10/anaconda/2023.03"

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
nnUNetv2_predict -d Dataset002_HCFC1 -i /work/shared/ngmm/3Dimage/DL_test/source_backgroundremoval/11-06-2024-1/ -o /work/shared/ngmm/3Dimage/DL_test/source_backgroundremoval/11-06-2024-1/pred -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_fullres -p nnUNetPlans
# Print a message indicating the end of the script's execution.
echo "Ending the shell .................."
