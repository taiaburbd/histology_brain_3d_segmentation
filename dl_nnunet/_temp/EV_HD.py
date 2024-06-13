import os
import nibabel as nib
import numpy as np 
from pathlib import Path
import json
import pandas as pd
from utils.helper import (
    convert_nrrd_to_nifti, create_folder, plot_all_slices, plot_histogram,
    generate_binary_image, adjust_affine_for_spacing_and_origin,
    save_binary_image_with_adjusted_origin, make_if_dont_exist
)
from utils.metrics import dice_score_per_class, hausdorff_distance_per_class, ravd_per_class

# Define dataset path
BASE_PATH = Path('./').resolve()
DATA_PATH = BASE_PATH / 'dataset'

project_name = 'HCFC1'  # Change here for different task name
task_name = 'Dataset002_' + project_name 

TRAINING_DATASET_PATH = BASE_PATH / 'dataset/nnUNet_raw_data' / task_name / 'imagesTr'
GT_TRAINING_DATASET_PATH = BASE_PATH / 'dataset/nnUNet_raw_data' / task_name / 'labelsTr'
TEST_DATASET_PATH = BASE_PATH / 'dataset/nnUNet_raw_data' / task_name / 'imagesTs'
GT_TEST_DATASET_PATH = BASE_PATH / 'dataset/nnUNet_raw_data' / task_name / 'labelsTs'
PREDICTION_RESULTS_PATH  = BASE_PATH / 'dataset/nnUNet_Prediction_Results' / task_name
TASK_PATH = BASE_PATH / 'dataset/nnUNet_raw_data' / task_name 

# Setup environment variables
nnUNet_raw = BASE_PATH / 'dataset/nnUNet_raw_data'
nnUNet_preprocessed = BASE_PATH / 'dataset/nnUNet_preprocessed'
nnUNet_results = BASE_PATH / 'dataset/nnUNet_results'

def read_nifti(path):
    img = nib.load(path)
    return img.get_fdata(), img.shape

ds_score = []
hd_score = []
havd_score = []

# Specify the path to your JSON file
json_file_path = TASK_PATH / 'dataset.json'

# Read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

labels = data['labels']
head = ['Fold'] + ['Volume ID'] + list(labels.keys())

ds_score.append(head)
hd_score.append(head)
havd_score.append(head)

dataset_config_path = f"{task_name}/nnUNetTrainer__nnUNetPlans__3d_fullres"
gtPath = GT_TRAINING_DATASET_PATH

for i in range(5):
    imagePath = f"/user1/ngmm/tr855969/Desktop/Taiabur/ngmm-nnunet/dataset/nnUNet_results/{dataset_config_path}/fold_{i}/validation"
    all_files = os.listdir(imagePath)
    all_files = sorted(all_files)
    
    for file in all_files:
        if file.endswith(".nii.gz"):
            imgP = os.path.join(imagePath, file)
            gtP = os.path.join(gtPath, file)
            # print(imgP)
            # print(gtP)
            imgData, i_ = read_nifti(imgP)
            gtData, g_ = read_nifti(gtP)
            newname = file.split("_")[0]
            print(newname)
            # print(i_)
            # print(g_)

            concatenated_array = np.concatenate(([i], [newname], dice_score_per_class(imgData, gtData, 25)))
            concatenated_array = np.transpose(concatenated_array)

            # ds_score.append(concatenated_array)
            hd_scores = hausdorff_distance_per_class(imgData, gtData, 25)
            hd_scores.insert(0, newname)
            hd_scores.insert(0, i)
            hd_score.append(hd_scores)
            # havd_score.append(ravd_per_class(imgData, gtData, 25))

def transpose_table(table):
    transposed_table = []

    # Get the header row and remove it from the table
    header = table.pop(0)
    # Initialize transposed table with the Volume ID column
    transposed_table.append(["Fold"] + [row[0] for row in table])

    # Transpose the table
    for i in range(1, len(header)):
        transposed_row = [header[i]]
        for j in range(len(table)):
            transposed_row.append(table[j][i])
        transposed_table.append(transposed_row)

    return transposed_table

# Transpose the table
data = transpose_table(hd_score) 

# Define column names
columns = ["Volume ID"] + [f"Value_{i}" for i in range(1, len(data[0]))]

# Create DataFrame
df = pd.DataFrame(data)

# Save DataFrame to Excel
df.to_excel(BASE_PATH / "data/full_resultaion_hausdorff_distance_dice.xlsx", index=False)

print("DataFrame saved to full_resultaion_hausdorff_distance_dice.xlsx")
