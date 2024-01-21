import numpy as np
import pandas as pd

# Get the blockmodel_avgs
blockmodel_avgs_df = pd.read_csv("blockmodel_avgs.csv").transpose()
raw_blockmodel_avgs = blockmodel_avgs_df.to_dict()

# Decode it into a nice easy to use datastructures
blockmodel_avgs = { raw_blockmodel_avg["block_name"]: np.array([raw_blockmodel_avg[i] for i in ['r', 'g', 'b', 'a']]) for raw_blockmodel_avg in raw_blockmodel_avgs.values() }
blockmodel_names, avgs = list(blockmodel_avgs.keys()), np.array(list(blockmodel_avgs.values()))

# Get the average color of a block (returns None if there isn't any)
def get_block_avg_color(blockname):
    return blockmodel_avgs.get(blockname)

# Get a block with the closest average to the specified color, its average, and the difference (there's no need to use a 16-tuple tree here so I didn't)
def get_closest_colored_block(color):
    # Convert the color to a numpy array if it isn't already
    if not isinstance(color, np.ndarray):
        color = np.array(color)

    distances = np.sqrt(np.sum((avgs - color) ** 2, axis=1))
    closests_index = np.argmin(distances)
    closest = blockmodel_names[closests_index]
    closest_avg = avgs[closests_index]
    distance = distances[closests_index]
    return (closest, closest_avg, distance)

# Get the blocks that have an exact color
def get_blocks_of_color(color):
    # Convert the color to a numpy array if it isn't already
    if not isinstance(color, np.ndarray):
        color = np.array(color)

    return [blockmodel_names[i] for i in np.nonzero((color == avgs).all(axis=1))[0]]