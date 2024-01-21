import blockmodel_avg_mapper as bam

# Get a list as input
def input_list(prompt):
    raw_vals = input(prompt).replace(' ', '').replace('(', '').replace(')', '').split(',')
    vals = []

    for raw_val in raw_vals:
        if not raw_val.replace('.', '', 1).isdigit():
            return None
        else:
            val = float(raw_val)
            vals.append(val)

    return vals

# The starting prompt
prompt = """Choose what you want to do:
    1. Get the average of a block
    2. Get one of the closest block to a color average
    3. Get the blocks with a specific color average

I choose option #"""
num_options = prompt.count("\n  ")

# The option chosen
option = input(prompt)

if not option.isdigit() or int(option) > num_options:
    print(f"You entered an INVALID option of: { option }\nYou have to choose a number between 1 & { num_options } (inclusive)")
    quit()

# Execute whatever option's chosen
print()
match int(option):
    case 1:
        res = input("Enter the name of the block that you'd like to find the average color of: ")
        color = bam.get_block_avg_color(res)
        if color is None:
            print("That block doesn't exist!")
        else:
            print(f"The { res } block's average color is { color }")
    case 2:
        res = input_list("Enter the RGBA color you want to get one of the closest blocks for: ")
        if res is None or len(res) != 4:
            print("Invalid RGBA value! (Format RGBA values like this: r, g, b, a)")
        else:
            block, color, difference = bam.get_closest_colored_block(res)
            print(f"The closest block I've found is the { block } block with a color of { color }. Their difference value is { difference }")
    case 3:
        res = input_list("Enter the RGBA color you want to get all of the blocks with it for: ")
        if res is None or len(res) != 4:
            print("Invalid RGBA value! (Format RGBA values like this: r, g, b, a)")
        else:
            blocks = bam.get_blocks_of_color(res)
            print(f"I've found { len(blocks) } blocks with the specified color:")
            for block in blocks:
                print(f"\t- { block }")