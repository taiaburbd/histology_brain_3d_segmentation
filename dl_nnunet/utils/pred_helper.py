import os
import nrrd
import os
from utils.helper import load_nifti_file,convert_file_format,file_exists, load_nifti_file_af_datatype
import nibabel as nib

def remove_nrrd_files(directory):
    """
    Removes all .nrrd files from the specified directory.

    Parameters:
    - directory: str, the path to the directory from which .nrrd files are to be deleted.
    """
    # Count of removed files
    removed_files = 0

    # List all files in the directory
    for file in os.listdir(directory):
        if file.endswith('.nrrd'):
            # Construct full file path
            file_path = os.path.join(directory, file)
            # Remove the file
            os.remove(file_path)
            removed_files += 1
            print(f"Removed: {file_path}")

    if removed_files == 0:
        print("No .nrrd files found to remove.")
    else:
        print(f"Total .nrrd files removed: {removed_files}")

def multiply_vol_save_nifti(source_path, binary_path, save_path):
    file_list = os.listdir(binary_path)
    for file in file_list:
        if file.endswith('.nii.gz'):
            binary_file = os.path.join(binary_path, file)
            
            new_file = file.replace(".nii.gz", "_0000.nii.gz")
            save_file = file.replace("_0000.nii.gz", ".nii.gz")
            
            source_file = os.path.join(source_path, new_file)
            print(source_file)
            save_vol = os.path.join(save_path, save_file)
            
            if file_exists(source_file) and file_exists(binary_file):
                source_data, s_shape, s_affine, s_datatype = load_nifti_file_af_datatype(source_file)
                binary_data, b_shape, b_affine, b_datatype = load_nifti_file_af_datatype(binary_file)
                
                new_data = source_data * binary_data

                # Convert the result to the appropriate data type
                new_data = new_data.astype(s_datatype)
                
                # Create a new NIfTI image
                new_img = nib.Nifti1Image(new_data, s_affine)

                # Save the new NIfTI image
                nib.save(new_img, save_vol)

                print('Saved successfully:', save_vol)
            else:
                print('File not exists:', source_file if not file_exists(source_file) else binary_file)



def multiply_vol_save_nrrd(source_path,binary_path, save_path):
    file_list = os.listdir(binary_path)
    for file in file_list:
        if file.endswith('.nii.gz'):

            new_file = file.replace(".nii.gz", "_0000.nii.gz")
            save_file = file.replace(".nii.gz", ".nrrd")

            source_file = os.path.join(source_path,new_file)
            binary_file = os.path.join(binary_path,file)
            save_vol = os.path.join(save_path,save_file)
            print(source_file)
            print(binary_file)
            if (file_exists(source_file) and file_exists(binary_file)):
                source_data,s_shape, s_affine,s_datatype= load_nifti_file_af_datatype(source_file)
                binary_data,b_shape,b_affine,b_datatype = load_nifti_file_af_datatype(binary_file)

                new_data = source_data * binary_data

                # Convert the NIfTI header to a NRRD-compatible format (if needed)
                nrrd_header = {
                    'type': str(source_data.dtype),
                    'dimension': len(s_shape),
                    'sizes': s_shape,
                    'kinds': ['domain', 'domain', 'domain'],
                    'space': 'left-posterior-superior',
                    'space directions': s_affine[:3, :3].tolist(),
                    'space origin': s_affine[:3, 3].tolist(),
                    'encoding': 'gzip'
                }

                nrrd.write(save_vol, new_data, nrrd_header)

                print('save successfully...', save_vol)
            else:
                print('file not exists')