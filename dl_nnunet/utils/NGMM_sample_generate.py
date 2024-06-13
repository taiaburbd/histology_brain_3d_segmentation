import argparse
from pathlib import Path
from utils.pred_helper import multiply_vol_save_nrrd

def main(source_path, binary_path, save_path):
    source_path = Path(source_path).resolve()
    binary_path = Path(binary_path).resolve()
    save_path = Path(save_path).resolve()

    if not source_path.exists():
        print(f"Error: The source path '{source_path}' does not exist.")
        return

    if not binary_path.exists():
        print(f"Error: The binary path '{binary_path}' does not exist.")
        return

    if not save_path.exists():
        print(f"Save path '{save_path}' does not exist. Creating it.")
        save_path.mkdir(parents=True, exist_ok=True)

    # Perform the multiplication and save as NIFTI
    multiply_vol_save_nrrd(source_path, binary_path, save_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate ROI samples and save as NIFTI.')
    parser.add_argument('--source_path', type=str, required=True, help='The source directory containing files to be processed.')
    parser.add_argument('--binary_path', type=str, required=True, help='The binary directory containing binary mask files.')
    parser.add_argument('--save_path', type=str, required=True, help='The directory where the processed NIFTI files will be saved.')

    args = parser.parse_args()

    main(args.source_path, args.binary_path, args.save_path)
