import numpy as np
import yaml, os, sys

from lib.utils import read_FitsCat, add_clusters_unique_id
from lib.utils import concatenate_cl_tiles
from lib.gawa import cl_duplicates_filtering


# read config files as online arguments 
config = sys.argv[1]
dconfig = sys.argv[2]
# read config file
with open(config) as fstream:
    param_cfg = yaml.safe_load(fstream)
with open(dconfig) as fstream:
    param_data = yaml.safe_load(fstream)
 
workdir = param_cfg['out_paths']['workdir']
out_paths = param_cfg['out_paths']
admin = param_cfg['admin']
gawa_cfg = param_cfg['gawa_cfg']
clcat = param_cfg['clcat']
clkeys = clcat['gawa']['keys']
tiles_filename = os.path.join(
    workdir, admin['tiling_gawa']['rpath'], 
    admin['tiling_gawa']['tiles_filename']
)
all_tiles = read_FitsCat(tiles_filename)

# concatenate all tiles
data_clusters0 = concatenate_cl_tiles(out_paths, all_tiles, 'gawa')

# final filtering 
data_clusters0f = cl_duplicates_filtering(
    data_clusters0, gawa_cfg, clkeys, 'survey'
)
# create unique index with decreasing SNR 
data_clusters = add_clusters_unique_id(data_clusters0f, clkeys)
data_clusters.write(clcat['gawa']['cat'], overwrite=True)
