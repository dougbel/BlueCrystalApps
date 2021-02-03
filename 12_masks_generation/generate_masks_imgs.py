import argparse
import logging
import os
import time
import traceback

import numpy as np
import pandas as pd
from PIL.Image import Image, fromarray
from mpi4py import MPI

from mpi_master_slave import WorkQueue, Master, Slave

parser = argparse.ArgumentParser()
parser.add_argument('--scannet_analysis_dir', required=True,
                    # default="/media/dougbel/Tezcatlipoca/dataset_analysis/mpi_routines",
                    help='Path to information generated by mpi routines')

# ["train", "test]
parser.add_argument('--stage', required=True,  # default="train",
                    help='Indicates if working with "train" or "test" data')

# ["all", "reaching_out", "laying", "basic_human_inter", "good_human_inter", "placing_boxes"]
parser.add_argument('--interactions_set', required=True,  # default="good_human_inter",
                    help='Indicate set of interactions to use')

parser.add_argument('--analysis_intersections_dir', required=True,  # default="./output/02_by_frame_analysis",
                    help='Path to the analysis of intersections')

parser.add_argument('--output_dir', required=True,
                    # default="/media/dougbel/Tezcatlipoca/dataset_analysis/mpi_routines/train_cnn",
                    help='Output dir')

parser.add_argument('--analysis_intersection_percentages', required=True,  # default="1to100",
                    help='1to100')

opt = parser.parse_args()
print(opt)


def get_interactions_name_in_subgroup(subgroup_name):
    subgroup = []
    if subgroup_name == "reaching_out":
        subgroup = ["reaching_out_low_human_reaching_out_low", "reaching_out_mid_low_human_reaching_out_mid_low",
                    "reaching_out_mid_up_human_reaching_out_mid_up", "reaching_out_up_human_reaching_out_up"]
    elif subgroup_name == "laying":
        subgroup = ["child_laying_child_laying", "laying_human_laying"]
    elif subgroup_name == "basic_human_inter":
        subgroup = ["child_laying_child_laying", "laying_human_laying",
                    "sitting_human_sitting", "standing_up_floor_human_standing_up",
                    "reaching_out_low_human_reaching_out_low", "reaching_out_mid_low_human_reaching_out_mid_low",
                    "reaching_out_mid_up_human_reaching_out_mid_up"]
    elif subgroup_name == "good_human_inter":
        subgroup = ["child_laying_child_laying", "laying_human_laying",
                    "sitting_human_sitting", "standing_up_floor_human_standing_up",
                    "reaching_out_low_human_reaching_out_low", "reaching_out_mid_low_human_reaching_out_mid_low"]
    elif subgroup_name == "placing_boxes":
        subgroup = ["placing_large_box_large_box", "placing_small_box_small_box"]
    elif subgroup_name == "all":
        subgroup = ["placing_large_box_large_box", "placing_small_box_small_box",
                    "child_laying_child_laying", "laying_human_laying",
                    "sitting_human_sitting", "standing_up_floor_human_standing_up",
                    "reaching_out_low_human_reaching_out_low", "reaching_out_mid_low_human_reaching_out_mid_low",
                    "reaching_out_mid_up_human_reaching_out_mid_up", "reaching_out_up_human_reaching_out_up"]

    return subgroup


class MasterMasksGenerationImgs(object):
    """
    This is my application that has a lot of work to do so it gives work to do
    to its slaves until all the work is done
    """

    def __init__(self, slaves, analysis_intersections_dir, analysis_intersection_percentages, stage, interactions_set,
                 output_dir):
        # when creating the Master we tell it what slaves it can handle
        self.master = Master(slaves)
        # WorkQueue is a convenient class that run slaves on a tasks queue
        self.work_queue = WorkQueue(self.master)
        self.analysis_intersections_dir = analysis_intersections_dir
        self.analysis_intersection_percentages = analysis_intersection_percentages
        self.stage = stage
        self.interactions_set = interactions_set
        self.output_dir = output_dir

        logging_file = os.path.join(analysis_intersections_dir, 'process_masks_generation.log')
        logging.basicConfig(filename=logging_file, filemode='a', level=logging.INFO,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        # Creating multiple scenes produces some harmless error messages, to AVOID
        logging.getLogger('pyembree').disabled = True

    def terminate_slaves(self):
        """
        Call this to make all slaves exit their run loop
        """
        self.master.terminate_slaves()

    def run(self):
        """
        This is the core of my application, keep starting slaves
        as long as there is work to do
        """
        dir_output = f"{self.output_dir}/{self.interactions_set}"
        dir_output_images = f"{dir_output}/{self.stage}_images"
        dir_output_masks = f"{dir_output}/annotation_{self.stage}_images_imgs"

        if not os.path.exists(dir_output_images):
            os.makedirs(dir_output_images)
        if not os.path.exists(dir_output_masks):
            os.makedirs(dir_output_masks)

        #
        # let's prepare our work queue. This can be built at initialization time
        # but it can also be added later as more work become available
        #
        interactions = get_interactions_name_in_subgroup(self.interactions_set)
        full_analysis_dir = f"{self.analysis_intersections_dir}/data_{self.stage}/{self.analysis_intersection_percentages}/coincidences_analysis"
        analysis_file = f"{full_analysis_dir}/{self.interactions_set}/{interactions[0]}_1to100.xlsx"

        df_coincidences = pd.read_excel(analysis_file, sheet_name='Coincidences_0', index_col=0)
        l_coincidences = df_coincidences.values.tolist()

        n_tuples_ready = 0
        n_tuples_all = len(l_coincidences)

        logging.info(f"Work to process: {n_tuples_all} coincidences in set: {self.interactions_set}")

        for d in l_coincidences:
            # 'data' will be passed to the slave and can be anything
            self.work_queue.add_work(data=d)

        #
        # Keeep starting slaves as long as there is work to do
        #
        while not self.work_queue.done():

            #
            # give more work to do to each idle slave (if any)
            #
            self.work_queue.do_work()

            #
            # reclaim returned data from completed slaves
            #

            for slave_return_data in self.work_queue.get_completed_work():
                done, scan, frame, pc_name, pc_rank, message = slave_return_data
                if done:
                    n_tuples_ready += 1
                    logging.info(
                        f'{n_tuples_ready}/{n_tuples_all}, name {pc_name} slave rank {pc_rank} masking "{scan}" frame {frame}, success: {done}')
                else:
                    logging.error(f'name {pc_name} slave rank {pc_rank} analysing "{scan}" frame {frame}": \n{message}')

            # sleep some time
            time.sleep(0.3)

        with open(f"{dir_output}/interactions_used.txt", "w") as fp:
            fp.writelines("\n".join(interactions))


class SlaveMasksGeneration(Slave):
    """
     A slave process extends Slave class, overrides the 'do_work' method
     and calls 'Slave.run'. The Master will do the rest
     """

    def __init__(self, scannet_analysis_dir, stage, interactions_set, output_dir):
        super().__init__()
        # This threshold is the same used during data analysis.
        # set originally on class mpi_routines.slavesSlaveAnalyser
        self.threshold = 0.2

        self.full_dir_data = f"{scannet_analysis_dir}/{stage}"

        dir_output = f"{output_dir}/{interactions_set}"
        self.dir_output_images = f"{dir_output}/{stage}_images"
        self.dir_output_masks_imgs = f"{dir_output}/annotation_{stage}_images_imgs"

        self.interactions = get_interactions_name_in_subgroup(interactions_set)

        self.rank = MPI.COMM_WORLD.Get_rank()
        self.name = MPI.Get_processor_name()

    def do_work(self, data):
        scene, frame = data
        try:
            # extracting image frame in PNG
            interaction = self.interactions[0]
            sub_path = os.path.join(self.full_dir_data, "frame_propagation", scene, f"{interaction}_img_segmentation_w224_x_h224")
            data_compiled = np.load(os.path.join(sub_path, "scores_1.npz"))
            scores = data_compiled[f"image_frame_{frame}_scores_1.npy.npy"]

            ann_img = np.zeros((224, 224, 3)).astype('uint8')
            ann_img[np.where(scores > self.threshold)] = 1
            output_subpath = os.path.join(self.dir_output_masks_imgs, interaction)
            if not os.path.exists(output_subpath):
                os.makedirs(output_subpath)
            file = os.path.join(output_subpath, scene + str(frame).zfill(4) + '.png')
            im = fromarray(ann_img)
            im.save(file)

            return True, scene, frame, self.name, self.rank, ""
        except:
            return False, scene, frame, self.name, self.rank, traceback.format_exc()


if __name__ == "__main__":

    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    print('***************************************************************************')
    print('I am  %s rank %d (total %d)' % (name, rank, size))
    print('***************************************************************************')

    if rank == 0:  # Master

        app = MasterMasksGenerationImgs(slaves=range(1, size),
                                        analysis_intersections_dir=opt.analysis_intersections_dir,
                                        analysis_intersection_percentages=opt.analysis_intersection_percentages,
                                        stage=opt.stage,
                                        interactions_set=opt.interactions_set,
                                        output_dir=opt.output_dir)
        app.run()
        app.terminate_slaves()

    else:  # Any slave

        SlaveMasksGeneration(scannet_analysis_dir=opt.scannet_analysis_dir,
                             stage=opt.stage,
                             interactions_set=opt.interactions_set,
                             output_dir=opt.output_dir).run()

    print('Task completed (rank %d)' % (rank))
