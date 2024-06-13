import os
import nibabel as nib
import numpy as np
from scipy.spatial.distance import directed_hausdorff
import pandas as pd
import matplotlib.pyplot as plt

def load_nifti_image(filepath):
    """
    Load a NIfTI image from the given file path.
    """
    nifti_image = nib.load(filepath)
    image_data = nifti_image.get_fdata()
    return image_data

def calculate_hausdorff_distance(region1, region2):
    """
    Calculate the Hausdorff Distance between two binary regions.
    """
    # Get the coordinates of the non-zero elements in the binary regions
    coords1 = np.column_stack(np.nonzero(region1))
    coords2 = np.column_stack(np.nonzero(region2))
    
    # Calculate the directed Hausdorff distances
    hd1 = directed_hausdorff(coords1, coords2)[0]
    hd2 = directed_hausdorff(coords2, coords1)[0]
    
    # The Hausdorff Distance is the maximum of the two directed distances
    hd = max(hd1, hd2)
    
    return hd

def calculate_hd_for_regions(image, ground_truth, num_regions):
    """
    Calculate the Hausdorff Distances for all regions in the image and ground truth, excluding background.
    """
    hausdorff_distances = []
    
    for region in range(1, num_regions + 1):  # Excluding region 0 which is background
        image_region = (image == region)
        ground_truth_region = (ground_truth == region)
        if np.any(image_region) and np.any(ground_truth_region):  # Only calculate if regions are non-empty
            hd = calculate_hausdorff_distance(image_region, ground_truth_region)
            hausdorff_distances.append(hd)
        else:
            hausdorff_distances.append(np.nan)  # Append NaN if region is empty
    
    return hausdorff_distances

def process_images_and_labels(image_dir, ground_truth_dir, num_regions, output_dir):
    """
    Process all image and ground truth pairs in the given directories and save the box plot.
    """
    columns = ["CTX+", "cc+", "CPu", "DG", "HP", "RHP", "A", "ig", "fi", "ac", "ic", "st", "f", "och", "fr", "Hb", "TH", "HY", "MB", "P", "MY", "TCB", "V", "OB"]
    all_distances = []

    for filename in os.listdir(image_dir):
        if filename.endswith(".nii") or filename.endswith(".nii.gz"):
            image_path = os.path.join(image_dir, filename)
            gtfilename = filename.replace("_0000","")
            ground_truth_path = os.path.join(ground_truth_dir, gtfilename)

            # Ensure corresponding ground truth exists
            if os.path.exists(ground_truth_path):
                print(f"Processing {filename}")
                image = load_nifti_image(image_path)
                ground_truth = load_nifti_image(ground_truth_path)

                # Calculate Hausdorff Distances for all regions
                hausdorff_distances = calculate_hd_for_regions(image, ground_truth, num_regions)
                all_distances.append([filename] + hausdorff_distances)
            else:
                print(f"Ground truth for {filename} not found.")

    # Check if distances were calculated
    if len(all_distances) == 0:
        print("No images processed. Please check your directories.")
        return

    # Convert all distances to a DataFrame
    columns = ["Filename"] + columns
    data = np.array(all_distances)
    df = pd.DataFrame(data, columns=columns)

    # Save DataFrame to Excel
    excel_output_path = os.path.join(output_dir, 'hausdorff_distances.xlsx')
    df.to_excel(excel_output_path, index=False)
    print(f"Data saved to {excel_output_path}")

    # Drop the Filename column for plotting
    df = df.drop(columns=["Filename"])

    # Create and save a decorative box plot
    plt.figure(figsize=(14, 10))
    box = df.boxplot(patch_artist=True)

    # Customizing the box plot
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700', '#FF6347', '#4682B4', '#8A2BE2', '#5F9EA0', '#D2691E', '#6495ED', '#DC143C', '#00FFFF', '#00008B', '#B8860B', '#006400', '#8B0000', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B4513', '#2E8B57', '#00FF7F', '#4682B4']

    for patch, color in zip(box.artists, colors):
        patch.set_facecolor(color)

    # Customizing the plot
    plt.xticks(rotation=90)  # Rotate x-axis labels
    plt.title('Box Plot of Hausdorff Distances by Region')
    plt.xlabel('Region')
    plt.ylabel('Hausdorff Distance')
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # Save plot
    plot_output_path = os.path.join(output_dir, 'hausdorff_distance_boxplot_hd.png')
    plt.savefig(plot_output_path)
    plt.close()
    print(f"Box plot saved to {plot_output_path}")


# Define directories
image_dir = '/user1/ngmm/tr855969/Desktop/Taiabur/ngmm-nnunet/dataset/nnUNet_raw_data/Dataset002_HCFC1/imagesTr'
ground_truth_dir = '/user1/ngmm/tr855969/Desktop/Taiabur/ngmm-nnunet/dataset/nnUNet_raw_data/Dataset002_HCFC1/labelsTr'
output_dir = 'data/'
num_regions = 24  # Excluding background

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process images and labels, then save the box plot
process_images_and_labels(image_dir, ground_truth_dir, num_regions, output_dir)
