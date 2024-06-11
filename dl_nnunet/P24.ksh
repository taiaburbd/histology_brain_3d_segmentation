#!/bin/bash

source /user1/ngmm/tr855969/.bashrc

conda activate /user1/ngmm/tr855969/.conda/envs/env_tf

# Assign the root directory path for the project to a variable.
MYROOTDIR="/user1/ngmm/tr855969/Desktop/Taiabur/ngmm-nnunet/"

cd $MYROOTDIR

nnUNet_raw="/beegfs/data/work/shared/ngmm/scripts/Taiabur/ngmm-nnunet/dataset/nnUNet_raw_data"
nnUNet_preprocessed="/beegfs/data/work/shared/ngmm/scripts/Taiabur/ngmm-nnunet/dataset/nnUNet_preprocessed"
nnUNet_results="/beegfs/data/work/shared/ngmm/scripts/Taiabur/ngmm-nnunet/dataset/nnUNet_results"

export nnUNet_raw=$nnUNet_raw
export nnUNet_preprocessed=$nnUNet_preprocessed
export nnUNet_results=$nnUNet_results

nnUNetv2_predict -d Dataset002_HCFC1 -i /work/shared/ngmm/3Dimage/DL_test/destination_backgroundremoval/volume/ -o /work/shared/ngmm/3Dimage/DL_test/target_seg_pred -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_lowres -p nnUNetPlans
# Print a message indicating the end of the script's execution.
echo "Ending the shell script"
