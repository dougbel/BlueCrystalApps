# BlueCrystalApps


### 10_mpi_analysis_dataset
Runs over MPI to perform the analysis of data over npz files after the data set was generated

Use comand:

    sbatch task_analysis_dataset.sh







### 12_masks_generation

Extract masks to be used for training, it uses an analysis of intersections (frames where two or more affordances are observed, see project _multilalbel_classifier/02_by_frame_analysis_info_tables_walterios_approach.py_)

##### Commands:

- Generate masks in form of numpy arrays with size *h,w,c* where every channel is the mask associated to the affordances in the set
	
	    sbatch generate_masks_imgs_ghi_test.sh 
	    
	    sbatch generate_masks_imgs_ghi_train.sh

- Extract only masks in form of images for a given set of affordances (ghi: good human interactions)
	
	    sbatch generate_masks_imgs_ghi_test.sh 
	    
	    sbatch generate_masks_imgs_ghi_train.sh
	    
	   
##### Defined set of affordances:
reaching_out

	"reaching_out_low_human_reaching_out_low", "reaching_out_mid_low_human_reaching_out_mid_low", "reaching_out_mid_up_human_reaching_out_mid_up", "reaching_out_up_human_reaching_out_up"


laying

	"child_laying_child_laying", "laying_human_laying"
	
        
basic_human_inter

	"child_laying_child_laying", "laying_human_laying", "sitting_human_sitting", "standing_up_floor_human_standing_up", "reaching_out_low_human_reaching_out_low", "reaching_out_mid_low_human_reaching_out_mid_low", "reaching_out_mid_up_human_reaching_out_mid_up"


***good_human_inter***

     "child_laying_child_laying", "laying_human_laying", "sitting_human_sitting", "standing_up_floor_human_standing_up", "reaching_out_low_human_reaching_out_low", "reaching_out_mid_low_human_reaching_out_mid_low"
                    
                    
placing_boxes:

     "placing_large_box_large_box", "placing_small_box_small_box
     
     
all:
 
      "placing_large_box_large_box", "placing_small_box_small_box", "child_laying_child_laying", "laying_human_laying", "sitting_human_sitting", "standing_up_floor_human_standing_up", "reaching_out_low_human_reaching_out_low", "reaching_out_mid_low_human_reaching_out_mid_low", "reaching_out_mid_up_human_reaching_out_mid_up", "reaching_out_up_human_reaching_out_up"]

