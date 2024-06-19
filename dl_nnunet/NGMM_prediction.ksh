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

# Activate a Conda environment named `env_tf`. 
# This prepares the shell with the environment's specific Python and library setup.
conda activate /user1/ngmm/tr855969/.conda/envs/env_tf

# Execute the nnUNet training command with specified parameters.
# This is likely a command specific to the nnUNet framework for medical image segmentation.

# config
binary_dataset="Dataset001_Wdr47Kusss"
roi_seg_dataset="Dataset002_HCFC1"
pred_config="3d_lowres"

# path setup


source_file_path="/work/shared/ngmm/3Dimage/DL_test/source_backgroundremoval/13-06-2024/"
temp_path="${source_file_path}/_temp"
prediction="${source_file_path}/prediction/"

converted_file_path="${temp_path}/1.VolumeReformat"
binary_prediction_path="${temp_path}/2.binary"
roi_source_file_path="${temp_path}/3.roi"
roi_seg_file_path="${temp_path}/4.roi_seg"
prediction_postprocessed="${temp_path}/5.postprocessed"



# File conversion
python utils/NGMM_convert.py --input_path ${source_file_path} --output_path ${converted_file_path}

echo "Step: 1/7 done"
# nnUNet prediction for binary segmentation
nnUNetv2_predict -d ${binary_dataset} -i ${converted_file_path} -o ${binary_prediction_path} -f 0 1 2 3 4 -tr nnUNetTrainer -c ${pred_config} -p nnUNetPlans

echo "Step: 2/7 done"
# Generate ROI samples
python utils/NGMM_sample_generate.py --source_path ${converted_file_path} --binary_path ${binary_prediction_path} --save_path ${roi_source_file_path}

echo "Step: 3/7 done"

# Convert ROI for further processing
python utils/NGMM_convert.py --input_path ${roi_source_file_path} --output_path ${roi_source_file_path}

echo "Step: 4/7 done"
# nnUNet prediction for ROI segmentation
nnUNetv2_predict -d ${roi_seg_dataset} -i ${roi_source_file_path} -o ${roi_seg_file_path} -f  0 1 2 3 4 -tr nnUNetTrainer -c ${pred_config} -p nnUNetPlans

echo "Step: 5/7 done"

# label define
python utils/processVolumes.py -i ${roi_seg_file_path} -o ${prediction}

echo "Step: 6/7 done"

# # remove temp file
python utils/remove_directory.py -i ${temp_path}

echo "Step: 7/7 done"
