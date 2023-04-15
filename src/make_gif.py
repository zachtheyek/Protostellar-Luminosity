from PIL import Image
import imageio
import random

# Open the input image and get its dimensions
input_image = Image.open("nobel.png")
width, height = input_image.size

# Set the size of the grid
grid_size = 20

# Calculate the dimensions of each grid element
grid_width = width // grid_size
grid_height = height // grid_size

# Create a list of all the grid positions
grid_positions = [(x, y) for x in range(grid_size) for y in range(grid_size)]

# Shuffle the grid positions
random.shuffle(grid_positions)

# Create a list to store the frames of the GIF
frames = []

# Create a new image with a black background
new_image = Image.new("RGB", (width, height), color=(0, 0, 0))

# Loop over each grid position
for i, position in enumerate(grid_positions):
    # Create a new image with a black background
    grid_image = Image.new("RGB", (grid_width, grid_height), color=(0, 0, 0))

    # Loop over each pixel in the current grid element
    for x in range(position[0] * grid_width, (position[0] + 1) * grid_width):
        for y in range(position[1] * grid_height, (position[1] + 1) * grid_height):
            # Get the pixel value from the input image
            pixel = input_image.getpixel((x, y))
            # Set the corresponding pixel in the grid image
            grid_image.putpixel((x - position[0] * grid_width, y - position[1] * grid_height), pixel)

    # Add the grid element to the new image
    new_image.paste(grid_image, (position[0] * grid_width, position[1] * grid_height))

    # Add the new image to the list of frames
    frames.append(new_image.copy())

    print(f'{i+1}/{grid_size*grid_size} done')

# Save the frames as a GIF
imageio.mimsave("nobel.gif", frames, duration=0.05)