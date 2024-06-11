# import lib
import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from pathlib import Path
import nrrd
import shutil
import json
import SimpleITK as sitk

#image convert to nifti from nrrd. 
def convert_nrrd_to_nifti(nrrd_file_path, nifti_file_path):
    # Read the NRRD file
    nrrd_data, nrrd_options = nrrd.read(nrrd_file_path)
        
    # Save the NIfTI image
    nib.save(nib.Nifti1Image(nrrd_data.astype(np.float32), affine=np.eye(4)), nifti_file_path)

# create directory
def create_folder(_dir):
    if not os.path.exists(_dir):
        os.makedirs(_dir)

# Function to plot all slices of a 3D image
def plot_all_slices(data):
    # Determine the number of slices to display
    slices = data.shape[-1]
    # Calculate the number of subplots needed (square root of number of slices, rounded up)
    subplot_dim = int(np.ceil(np.sqrt(slices)))
    fig, ax = plt.subplots(subplot_dim, subplot_dim, figsize=(15, 15))
    ax = ax.flatten()
    for i in range(slices):
        ax[i].imshow(data[:, :, i], cmap='gray')
        ax[i].axis('off')
    # Hide any unused subplots
    for i in range(slices, len(ax)):
        ax[i].axis('off')
    plt.show()

# Function to plot histogram of voxel intensities
def plot_histogram(data):
    fig, ax = plt.subplots()
    ax.hist(data.ravel(), bins=256, color='c', alpha=0.75)
    ax.set_xlabel('Intensity Value')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Voxel Intensities')
    plt.show()

# Function to generate a binary image based on a threshold
def generate_binary_image(data, threshold):
    binary_data = np.where(data > threshold, 0, 1)
    return binary_data

# Function to adjust voxel spacing and set the origin to 0
def adjust_affine_for_spacing_and_origin(affine):
    # Create a new affine matrix with 1mm spacing if not already set
    new_affine = affine.copy()
    np.fill_diagonal(new_affine[:3, :3], 1)
    # Set the origin to 0
    new_affine[:3, 3] = 0
    return new_affine

# Function to save binary data as a new NIfTI image with 1mm³ voxel spacing and origin set to 0
def save_binary_image_with_adjusted_origin(binary_data, original_nii, output_filename):
    # Adjust affine for 1mm³ voxel spacing and set the origin to 0
    adjusted_affine = adjust_affine_for_spacing_and_origin(original_nii.affine)
    
    # Ensure the header is copied and modified for the new image dimensions
    new_header = original_nii.header.copy()
    new_header.set_zooms((1, 1, 1))  # Set voxel sizes to 1mm³
    
    # Create a NIfTI image from the binary data with adjusted affine
    binary_img = nib.Nifti1Image(binary_data.astype(np.int16), adjusted_affine, new_header)
    
    # Save the binary image to disk with the specified filename
    nib.save(binary_img, output_filename + '.nii.gz')

def make_if_dont_exist(folder_path,overwrite=False):

    if os.path.exists(folder_path):
        
        if not overwrite:
            print(f'{folder_path} exists.')
        else:
            print(f"{folder_path} overwritten")
            shutil.rmtree(folder_path)
            os.makedirs(folder_path)

    else:
      os.makedirs(folder_path)
      print(f"{folder_path} created!")


# .nrrd to nifit.
def convert_file_format(ORG_DATA_PATH, OUT_DATA_PATH, endswith):
    all_files = os.listdir(ORG_DATA_PATH)
    for file in all_files:
        if file.endswith(endswith):
            source_nrrd_file_path = os.path.join(ORG_DATA_PATH, file)
            save_nifti_file_path = os.path.join(OUT_DATA_PATH, file)
            # Automatically generate the nifti_file_path based on nrrd_file_path
            base_name = os.path.splitext(os.path.basename(save_nifti_file_path))[0]
            # print(base_name)
            newname = os.path.splitext(os.path.basename(base_name))[0]
            # print(newname)
            save_nifti_file_path = os.path.join(os.path.dirname(save_nifti_file_path), newname + '_0000.nii.gz')
            # print(source_nrrd_file_path)
            # print(save_nifti_file_path)
            convert_nrrd_to_nifti(source_nrrd_file_path, save_nifti_file_path)
    print('File convert done. ')

def load_nifti_file(filepath):
    nifti_img = nib.load(filepath)
    return nifti_img, nifti_img.get_fdata(), 

def load_nifti_file_af_datatype(filepath):
    img = nib.load(filepath)
    data = img.get_fdata()
    shape = img.shape
    affine = img.affine
    datatype = img.get_data_dtype()
    return data, shape, affine, datatype

def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False


def print_nrrd_header_info(file_path):
    # Load the .seg.nrrd file using SimpleITK
    img = sitk.ReadImage(file_path)
    
    # Print all metadata keys and values
    print("Header Information:")
    for key in img.GetMetaDataKeys():
        print(f"{key}: {img.GetMetaData(key)}")
        
def read_and_display_json(file_path):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Pretty print the JSON data
    return data

def convert_nifti_to_seg_nrrd(input_filepath, output_filepath, labels):
    # Load the .nii.gz file using nibabel
    nii_img = nib.load(input_filepath)
    img_data = nii_img.get_fdata()

    # Create a SimpleITK image from the numpy array
    sitk_img = sitk.GetImageFromArray(np.transpose(img_data, (2, 1, 0)))
    sitk_img = sitk.Cast(sitk_img, sitk.sitkInt32)

    # Set the spacing (voxel sizes)
    spacing = nii_img.header.get_zooms()[:3]
    sitk_img.SetSpacing([float(sp) for sp in spacing])

    # Set the direction (rotation matrix)
    direction = np.linalg.inv(nii_img.affine[:3, :3]).flatten()
    sitk_img.SetDirection(direction.tolist())

    # Set the origin (translation vector)
    origin = nii_img.affine[:3, 3]
    sitk_img.SetOrigin(origin.tolist())

    # Add custom metadata for segments
    for i, label in enumerate(labels):
        sitk_img.SetMetaData(f"Segment{i}_ID", str(i))
        sitk_img.SetMetaData(f"Segment{i}_Name", label)
        sitk_img.SetMetaData(f"Segment{i}_ColorAutoGenerated", str(0))
        sitk_img.SetMetaData(f"Segment{i}_LabelValue", str(i))
        sitk_img.SetMetaData(f"Segment{i}_Layer", str(0))

    # Save the image as a .seg.nrrd file
    sitk.WriteImage(sitk_img, output_filepath, useCompression=True)
    print(f"Segmented NRRD file saved to: {output_filepath}")

def process_all_volumes(input_dir, output_dir, output_extension, labels):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".nii.gz"):
            input_filepath = os.path.join(input_dir, filename)
            output_filename = filename.replace(".nii.gz", output_extension)
            output_filepath = os.path.join(output_dir, output_filename)
            
            convert_nifti_to_seg_nrrd(input_filepath, output_filepath, labels)