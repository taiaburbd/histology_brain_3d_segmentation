#!/bin/bash

# exec bash
source /user1/ngmm/tr855969/.bashrc
# Print a message indicating the start of the script execution.
echo "Starting my shell script"

# Assign the path or name of the PyTorch module to a variable.
MY_PYTORCH_MODULE="pytorch/1.11.0/cuda/11.3.1/gpu"

# Assign the path or name of the Python module to a variable.
# MY_PYTHON_MODULE="python/3.10/anaconda/2023.03"

# Assign the root directory path for the project to a variable.
MYROOTDIR="/user1/ngmm/tr855969/Desktop/Taiabur/ngmm-nnunet/"

# Load the PyTorch module using the module management system.
module load ${MY_PYTORCH_MODULE}

# Load the Python module using the module management system.
# module load ${MY_PYTHON_MODULE}

# Change the current working directory to the project root directory.
# If changing the directory fails (e.g., the directory does not exist), exit the script to avoid further errors.
# cd $MYROOTDIR || exit
cd $MYROOTDIR
# Initialize Conda for the bash shell. This updates the shell to use Conda commands.
# It's necessary only once per shell type but included here to ensure Conda functions are available.
# conda init ksh

# Start a new instance of the bash shell. 
# This command is not typically used after `conda init` since `conda init` itself suggests restarting the shell.
# bash

# Replace the current shell process with a new bash shell. This is effectively a shell restart.
# This line seems redundant given the previous `bash` command and might not behave as expected in a script.
# exec bash

# Activate a Conda environment named `env_tf`. 
# This prepares the shell with the environment's specific Python and library setup.
conda activate /user1/ngmm/tr855969/.conda/envs/env_tf

# Execute the nnUNet training command with specified parameters.
# This is likely a command specific to the nnUNet framework for medical image segmentation.
nnUNetv2_train 3 3d_lowres 1 --npz


# Run the Python version command and redirect its output to a file named versions_YYYY-MM-DD_HH-MM-SS.txt.

# Print a message indicating the end of the script's execution.
echo "Ending the shell "
