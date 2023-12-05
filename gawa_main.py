import numpy as np
import yaml, os, sys

from lib.utils import create_mosaic_footprint, sky_partition
from lib.utils import slurm_submit

from lib.gawa import update_config, merged_cmd_polygons
from lib.gawa import compute_cmd_masks, compute_dslices
from lib.gawa import plot_all_cmds
from lib.gawa import create_gawa_directories, store_gawa_confs

# read config file as online argument 
config = sys.argv[1]
dconfig = sys.argv[2]

# open config files
with open(config) as fstream:
    param_cfg = yaml.safe_load(fstream)
with open(dconfig) as fstream:
    param_data = yaml.safe_load(fstream)
globals().update(param_data)

# Working & output directories 
survey = param_cfg['survey']
workdir = param_cfg['out_paths']['workdir']
create_gawa_directories(workdir)

# log message
print ('Gawa run on survey : ', survey)
print ('....... ref filter = ', param_cfg['ref_filter'])
print ('workdir : ', workdir)

# update param_data &  config (ref_filter, etc.)
param_cfg, param_data = update_config(param_cfg, param_data)

# create required data structure if not exist and update config 
if not input_data_structure[survey]['footprint_hpx_mosaic']:
    create_mosaic_footprint(
        footprint[survey], os.path.join(workdir, 'footprint')
    )
    param_data['footprint'][survey]['mosaic']['dir'] = os.path.join(
        workdir, 'footprint'
    )
    
# store config file in workdir
config, dconfig = store_gawa_confs(workdir, param_cfg, param_data)

# useful keys 
admin = param_cfg['admin']
gawa_cfg = param_cfg['gawa_cfg']

# slicing and associated diagnostic plots
compute_dslices(isochrone_masks[survey], gawa_cfg['dslices'],
                param_cfg['maglim_det'], workdir)
compute_cmd_masks(isochrone_masks[survey], param_cfg['out_paths'], gawa_cfg)
plot_all_cmds(
    gawa_cfg['dslices']['dslices_filename'], 
    isochrone_masks[survey], gawa_cfg['mask_resolution'],
    param_cfg['out_paths'],
    os.path.join(workdir, 'isochrone_masks', 'all_masks.png')
)

# partition for detection
ntiles = sky_partition(
    admin['tiling_gawa'], 
    param_data['starcat'][survey]['mosaic']['dir'],
    param_data['footprint'][survey], workdir
)

# run detection 
print ('Run wazp_tile / slurm ')
job_id1 = slurm_submit(
    'gawa_tile', config, dconfig, narray=ntiles
)
# concatenate 
job_id2 = slurm_submit(
    'gawa_concatenate', config, dconfig, dep=job_id1
)

print ('all done folks !')

