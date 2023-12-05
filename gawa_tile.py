import numpy as np
import yaml, os, sys

from lib.utils import read_FitsCat, create_tile_specs
from lib.gawa import gawa_tile

# read config files as online arguments 
config = sys.argv[1]
dconfig = sys.argv[2]
tile_id = int(sys.argv[3])

# read config file
with open(config) as fstream:
    param_cfg = yaml.safe_load(fstream)
with open(dconfig) as fstream:
    param_data = yaml.safe_load(fstream)

# load config info
survey, ref_filter  = param_cfg['survey'], param_cfg['ref_filter']
maglim_det = param_cfg['maglim_det']
starcat = param_data['starcat'][survey]
clcat = param_cfg['clcat']
out_paths = param_cfg['out_paths']
admin = param_cfg['admin']
footprint = param_data['footprint'][survey]
isochrone_masks = param_data['isochrone_masks'][survey]
gawa_cfg = param_cfg['gawa_cfg']
clkeys = param_cfg['clcat']['gawa']['keys']

# load tiles info
workdir = out_paths['workdir']
all_tiles = read_FitsCat(
    os.path.join(
        workdir, admin['tiling_gawa']['rpath'],
        admin['tiling_gawa']['tiles_filename'])
)
hpix_tile_lists = np.load(
    os.path.join(
        workdir, admin['tiling_gawa']['rpath'],
        admin['tiling_gawa']['tiles_npy']
    ), 
    allow_pickle=True
)
hpix_core_lists = np.load(
    os.path.join(
        workdir, admin['tiling_gawa']['rpath'],
        admin['tiling_gawa']['sky_partition_npy']
    ), 
    allow_pickle=True
)

# generate tile specs and run detection
tile_specs = create_tile_specs(
    admin['target_mode'], admin['tiling_gawa'],
    all_tiles[tile_id],  
    hpix_core_lists[tile_id], hpix_tile_lists[tile_id]
)
gawa_tile(
    admin, tile_specs,
    isochrone_masks,
    starcat, footprint, maglim_det, 
    gawa_cfg, clkeys, 
    out_paths, param_cfg['verbose']
)
