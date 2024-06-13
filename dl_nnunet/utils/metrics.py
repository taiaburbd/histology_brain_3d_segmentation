import numpy as np
from scipy.spatial.distance import directed_hausdorff

N_CLASSES = 2

#Dice score
def dice_score_per_class(segmented, ground_truth, num_classes=N_CLASSES):
    dice_scores = []
    for class_label in range(num_classes):
        # if class_label != 1:
            seg_binary = (segmented == class_label)
            gt_binary = (ground_truth == class_label)
            intersection = np.sum(seg_binary & gt_binary)
            sum_ = np.sum(seg_binary) + np.sum(gt_binary)
            dice_score = (2. * intersection) / sum_ if sum_ != 0 else 1
            dice_score = f"{dice_score:.4f}"
            dice_scores.append(dice_score)
    return dice_scores

# Hausdorff Distance (HD)
def hausdorff_distance_per_class(pred, gt, num_classes):
    hd_per_class = []

    for c in range(num_classes):
        pred_c = (pred == c)
        gt_c = (gt == c)

        if np.any(pred_c) and np.any(gt_c):
            pred_coords = np.column_stack(np.where(pred_c))
            gt_coords = np.column_stack(np.where(gt_c))
            hd = max(directed_hausdorff(pred_coords, gt_coords)[0], directed_hausdorff(gt_coords, pred_coords)[0])
        else:
            hd = np.nan  # Handle empty predictions or ground truth

        hd_per_class.append(hd)

    return hd_per_class


# Relative Absolute Volume Difference (RAVD)
def ravd_per_class(segmented, ground_truth, num_classes=N_CLASSES):
    ravd_scores = []
    for class_label in range(num_classes):
        # if class_label != 1:
            seg_binary = (segmented == class_label)
            gt_binary = (ground_truth == class_label)
            ravd = abs(np.sum(seg_binary) - np.sum(gt_binary)) / np.sum(gt_binary) if np.sum(gt_binary) != 0 else 0
            ravd_scores = f"{ravd:.4f}"
            ravd_scores.append(ravd)
    return ravd_scores