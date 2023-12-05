# gawa_slurm version 1.0

## gawa_slurm short description

This is a code intended to identify and qualify stellar clusters in large multi-band photometric surveys. 


## GAWA workflow 

1. computation of distance slicing based on
   a CMD mask and photometric errors
2. tilings of the sky - including overlaps
   * wtiles for detection
3. computation of global survey quantities
4. for each wtile 
   * loop over distance slices for detection
   * merge detections over slices 
5. concatenate detections over all tiles 
6. merge detections 


## GAWA with SLURM

The division of the sky in tiles offers an easy way to parallelize the code, which is now orchestrated by SLURM.

gawa_main generates and launches 2 sbatch scripts in array mode with dependencie:
   * gawa_tile 
   * gawa_concatenate 


## Installation 

Clone the repository and create an environment with Conda:
```bash
git clone https://github.com/linea-it/gawa_slurm && cd gawa_slurm 
conda create -n gawa python=3.11
conda activate gawa
pip install healpy
pip install scikit-image
pip install -U scikit-learn
conda install -c conda-forge cfitsio=3.430
conda install -c cta-observatory sparse2d
conda install -c conda-forge shapely
```


