import os
import nibabel as nib
import numpy as np
import argparse
from pathlib import Path
from utils.helper import convert_nrrd_to_nifti, create_folder, plot_all_slices, plot_histogram, generate_binary_image, adjust_affine_for_spacing_and_origin, save_binary_image_with_adjusted_origin, make_if_dont_exist, load_nifti_file, convert_file_format, file_exists, load_nifti_file_af_datatype
from utils.metrics import dice_score_per_class, hausdorff_distance_per_class, ravd_per_class
from utils.pred_helper import remove_nrrd_files, multiply_vol_save_nifti, multiply_vol_save_nrrd

def main(input_path, output_path, file_extension):
    input_path = Path(input_path).resolve()
    if output_path is None:
        output_path = input_path / 'VolumeReformat'

    else:
        output_path = Path(output_path).resolve()

    # create output Path
    output_path.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"Error: The input path '{input_path}' does not exist.")
        return

    if not output_path.exists():
        print(f"Output path '{output_path}' does not exist. Creating it.")
        output_path.mkdir(parents=True, exist_ok=True)

    # Perform the file conversion
    convert_file_format(input_path, output_path, file_extension)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert medical image file formats.')
    parser.add_argument('--input_path', type=str, required=True, help='The input directory containing files to be converted.')
    parser.add_argument('--output_path', type=str, help='The output directory where converted files will be saved. If not provided, "VolumeReformat" will be added to the input path.')
    parser.add_argument('--file_extension', type=str, default='.nrrd', help='The file extension of files to be converted (default: .nrrd).')

    args = parser.parse_args()

    main(args.input_path, args.output_path, args.file_extension)