import os
import shutil

origin_dir = "/mnt/storage/scratch/csapo/ScanNet_analysis_sitting"
dest_dir = "/mnt/storage/scratch/csapo/ScanNet_analysis_sitting/sum"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

#all directories of
for task in os.listdir(origin_dir):
    for output_subdir in os.listdir(os.path.join(origin_dir, task)):
        if not os.path.isfile(os.path.join(origin_dir, task, output_subdir)):
            #if "invalid_pose_" in output_subdir:
            if "_img_segmentation_" in output_subdir:
                for scan in os.listdir(os.path.join(origin_dir, task, output_subdir)):
                    original = os.path.join(origin_dir, task, output_subdir, scan)
                    target = os.path.join(dest_dir,output_subdir, scan)
                    print("from ",original, " to ",  target)
                    # shutil.move(original, target)