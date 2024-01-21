import os
import glob
from PIL import Image
import json
import numpy as np
import pandas as pd

# Check whether or not the data's be extracted
if not os.path.isdir("extracted-data"):
    raise Exception("The Minecraft assets directory extracted-data couldn't be found!") 

# Directories

# Where all the assets are
assets_dir = "extracted-data/assets/minecraft"
# Directory for all blockstates
blockstates_dir = f"{ assets_dir }/blockstates/*.json"
# Directory for block models
blockmodels_dir = f"{ assets_dir }/models/block/*.json"
# Directory for block textures
block_textures_dir = f"{ assets_dir }/textures/block/*.png"


# Functions

# Get the average color of an image
def avg_color(image_dir):
    # Get the image & make sure it's RGBA
    image = Image.open(image_dir).convert("RGBA")
    # Resize the image to 1x1 and get the color of it to get the avg
    avg_color = image.resize((1, 1)).getpixel((0, 0))
    return np.array(avg_color, dtype=np.float64)


# Lambdas

# Convert the Minecraft ID to a name
get_mc_id_name = lambda mc_texture: mc_texture[mc_texture.rfind('/') + 1:]
# Get just the blockstate's name from it's directory
get_blockstate_name = lambda model_dir: model_dir[model_dir.rfind('/', 0, -5) + 1:-5]
# Get just the name of the model from it's directory
get_model_name = lambda model_dir: model_dir[model_dir.rfind('/', 0, -5) + 1:-5]
# Get just the name of the texture from it's directory
get_texture_name = lambda texture_dir: texture_dir[texture_dir.rfind('/', 0, -4) + 1:-4]
# Keeps lists as lists and puts non-lists in a list
list_out = lambda x: x if type(x) is list else [x]


# Globals

# Get all the blockstates' name & values
blockstates = { get_blockstate_name(blockstate_dir): json.load(open(blockstate_dir)) for blockstate_dir in glob.glob(blockstates_dir) }
# Get all the models' names & values (some will not have textures attached to them since they're generic models)
blockmodels = { get_model_name(blockmodel_dir): json.load(open(blockmodel_dir)).get("textures") for blockmodel_dir in glob.glob(blockmodels_dir) }
# Get all the textures' names & average colors in key & value pairs
block_textures_avgs = { get_texture_name(block_texture_dir): avg_color(block_texture_dir) for block_texture_dir in glob.glob(block_textures_dir) }

# Get all the 
blockmodels_avgs = {}

# Main code
# Make it so that it doesn't use the whole directory

for blockstate_name, blockstate in blockstates.items():
    # The 2 possible locations containing the models
    variants = blockstate.get("variants")
    multipart = blockstate.get("multipart")

    # Get the model names from the blockstate as a list
    # then parse out the names (only the first variant & multipart get chosen since the rest are mostly unnecessary)
    model_names = [get_mc_id_name(mc_model["model"]) for mc_model in list_out(list(variants.values())[0] if multipart is None else multipart[0]["apply"])]

    # The sum that will be used to calculate the average
    sum = np.zeros((4), dtype=np.float64)
    # The number of textures which will be divided against sum to get the average
    num_textures = 0
    # Get the block models from the names (air blocks don't have a texture so they'll come up as None)
    for model_name in model_names:
        blockmodel = blockmodels[model_name]
        # Do something different for when it's none
        if blockmodels[model_name] is None:
            break

        # Add to the average
        for texture_key, mc_texture in blockmodel.items():
            # Some start with # and some just don't have matching textures so just don't add anything if None
            texture_avg = block_textures_avgs.get(get_mc_id_name(mc_texture))
            if texture_avg is None:
                continue
            num_textures += 1
            sum = np.add(sum, texture_avg)

    # Add the average if the blocks is visible (aka it has textures)
    avg = np.divide(sum, float(num_textures)) if num_textures != 0 else np.zeros([4])
    blockmodels_avgs[blockstate_name] = avg

# Write the blockmodel averages to blockmodel_avgs.csv
df = pd.DataFrame.from_dict(blockmodels_avgs, orient='index', columns=['r', 'g', 'b', 'a'])
df.index.name = "block_name"
df = df.sort_index()
df.to_csv("blockmodel_avgs.csv")
print("blockmodel_avgs.csv has been generated!")