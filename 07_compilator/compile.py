"""
Join outputs of and interaction analysis performed by a in a paralelized way as is Blue Crystal
"""
import os
import argparse
import shutil
import datetime

import pandas as pd

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True, help='Diretory with series of task')
    parser.add_argument('--output_dir', required=True, help='Directory with compilation')
    # parser.add_argument('--override', required=True, default=False, help='Override directories if exists')
    opt = parser.parse_args()
    print(opt)
    if not os.path.exists(opt.input_dir):
        print('Input dir unavailable')
    if not os.path.exists(opt.output_dir):
        print('Output dir unavailable')

    output_dir = opt.output_dir
    input_dir = opt.input_dir

    list_tasks = os.listdir(input_dir)
    list_tasks.sort()

    ##############################################################################################################
    # join all follow_up_process.csv files
    full_follow_up_process = pd.DataFrame()
    for task_dir in list_tasks:
        full_task_dir = os.path.join(input_dir, task_dir)
        df = pd.read_csv(os.path.join(full_task_dir, "follow_up_process.csv"), index_col=0)
        if full_follow_up_process.size == 0:
            full_follow_up_process = df
        else:
            full_follow_up_process.append(df)

    if os.path.isfile(os.path.join(output_dir, "follow_up_process.csv")):
        old_follow_up_file = os.path.join(output_dir, "follow_up_process.csv")
        old_follow_up = pd.read_csv( old_follow_up_file, index_col=0)
        full_follow_up_process = pd.merge(old_follow_up, full_follow_up_process,how='outer', left_index= True, right_index=True,
                                 on=['registered', 'environment', 'num_scan', 'sens_file', 'env_file', 'total_frames'])

        # new_follow_up.to_csv(os.path.join(output_dir, "new_follow_up.csv"))
        now = datetime.datetime.now()
        backup_file = "follow_up_process_backup%02d%02d%02d.csv" % (now.year, now.month, now.day)
        shutil.move(old_follow_up_file, os.path.join(output_dir, backup_file))


    full_follow_up_process.to_csv(os.path.join(output_dir, "follow_up_process.csv"))

    print("Concatenating follow_up_process.csv")


    ##############################################################################################################
    # get interactions and directories with propagation in rgb images

    task_dir = os.path.join(input_dir, list_tasks[0])
    internal_list = os.listdir(task_dir)
    subdir_interactions = []
    subdir_rgb_propagations = []
    for pseudo_interaction in internal_list:
        for to_test in internal_list:
            if pseudo_interaction != to_test and to_test.find(pseudo_interaction) != -1:
                subdir_interactions.append(pseudo_interaction)
                subdir_rgb_propagations.append(to_test)

    subdir_interactions = list(dict.fromkeys(subdir_interactions))
    subdir_rgb_propagations = list(dict.fromkeys(subdir_rgb_propagations))

    print(subdir_interactions)
    print(subdir_rgb_propagations)

    already_interactions = []
    for subdir_inter in subdir_interactions:
        full_subdir_inter = os.path.join(output_dir, subdir_inter)

        if os.path.exists(full_subdir_inter):
            print("Directory ", full_subdir_inter, " already exists")
            already_interactions.append(subdir_inter)
        else:
            os.makedirs(full_subdir_inter)
            print("Creating ", full_subdir_inter)
            task_scans = os.listdir(full_subdir_inter)
            for task in list_tasks:
                orig = os.path.join(input_dir, task, subdir_inter)
                dest = os.path.join(output_dir, subdir_inter)
                for scan in os.listdir(os.path.join(orig)):
                    shutil.copytree(os.path.join(orig, scan), os.path.join(dest, scan))
                print("From: ", orig, "  ---  to : ", dest)

    already_rgb_propagations = []
    for subdir_rgb_prop in subdir_rgb_propagations:
        full_subdir_rgb_prop = os.path.join(output_dir, subdir_rgb_prop)

        if os.path.exists(full_subdir_rgb_prop):
            print("Directory ", full_subdir_rgb_prop, " already exists")
            already_rgb_propagations.append(subdir_rgb_prop)
        else:
            os.makedirs(full_subdir_rgb_prop)
            print("Creating ", full_subdir_rgb_prop)
            task_scans = os.listdir(full_subdir_rgb_prop)
            for task in list_tasks:
                orig = os.path.join(input_dir, task, subdir_rgb_prop)
                dest = os.path.join(output_dir, subdir_rgb_prop)
                for scan in os.listdir(os.path.join(orig)):
                    shutil.copytree(os.path.join(orig, scan), os.path.join(dest, scan))
                print("From: ", orig, "  ---  to : ", dest)

    if len(already_interactions) > 0 or len(already_rgb_propagations)>0 :
        print("##########################################################################")
        print("WARNING!: ")
        print("Interactions not compiled as the output directory already existed")
        print(already_interactions)
        print("Directory of propagation in RGB images not compiled as the output directory already existed")
        print(already_rgb_propagations)
