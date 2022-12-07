# Used to list images in a folder
import os
# Used to read and edit image files
from PIL import Image
# Used to select random pixels for random sample
from random import randint
# Used to process random sample for most common pixel
from collections import Counter

# I found out the background green differs from picture to picture... so we will edit this later
backgroundColor = (0, 0, 0)


# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
formats = {
    "green": "\x1b[0;92;48m",
    "white": "\x1b[0;97;48m"
}


# Tests if the given pixel in (r,g,b) format is within a tolerable range
# @param Tuple rgb (r, g, b) pixel to test
# @param float leniency tolerance percent
# @returns Boolean if the given pixel is in the margin of error of background color
def is_background_color(rgb, leniency = 0.4):
    # testing for low red values
    same = backgroundColor[0] * (1+leniency) >= rgb[0]
    # Testing for high green values
    same = same and backgroundColor[1] * (1-leniency) <= rgb[1]
    # testing for low blue values
    same = same and backgroundColor[2] * (1+leniency) >= rgb[2]

    return same


# Takes a random sample and organizes it in a dictionary sorted by frequency
# @param List pixels [(r, g, b)] list of all pixels to test in 2d list
# @param Int width the width of the image
# @param Int height the height of the image
# @param Int tests optional the number of pixels to sample
# @returns Dictionary each color as key and value is number of occurrences
def sample(pixels, width, height, tests = 500):
    gathered = []

    # For each test, pick a random pixel and add it to gathered
    for j in range(tests):
        gathered.append(pixels[randint(0, width-1), randint(0, height-1)])

    # Counter iterates through a list, creating the dictionary with occurrences of each key
    return Counter(gathered)


# Averages the color of each pixel in the list
# @param List pixels [(r, g, b)] list of all pixels blur together
def blur_rgb(pixels):
    # start with first pixel - it will be used twice to weight favor towards it
    r, g, b = pixels[0]

    # for each pixel
    for j in range(len(pixels)):
        r, g, b = pixels[j]  # get its pixels
        r = (r * j + r) / (j + 1)  # this is an average that gives equal weight to each pixel
        g = (g * j + g) / (j + 1)
        b = (b * j + b) / (j + 1)

    # returns a tuple of the 3 newly averaged pixels
    return int(r), int(g), int(b)


# Takes a random sample and organizes it in a dictionary sorted by frequency
# @param Image image Pillow object, used to display the image
# @param List pixels [(r, g, b)] list of all pixels to test in 2d list
# @param String name name of the file these pixels belong to
def shader(image, pixels, name):
    # show this image and ask if we want to change it
    image.show()
    while "y" in get_input(f"{formats['white']}\n\nYou have selected {formats['green']}{name}{formats['white']}. "
                           "Would you like to edit this image? (y/n)").lower():

        # value multiplied to each color
        darken = float(get_input("Decimal percent to lighten or darken (0 = all black, 1 do nothing, 2 doubles): ")
                       .strip())
        # value to multiply the red component by
        red = float(get_input("Decimal percent to change red (0.0 = removes red, 1 do nothing, 2.0 doubles): ")
                    .strip())
        # value to multiply the green component by
        green = float(get_input("Decimal percent to change green (0.0 = removes green, 1 do nothing, 2.0 doubles): ")
                      .strip())
        # value to multiply the blue component by
        blue = float(get_input("Decimal percent to change blue (0.0 = removes blue, 1 do nothing, 2.0 doubles): ")
                     .strip())

        # iterate over the entire image
        for j in range(bw-1):
            for k in range(bh-1):
                # get current pixel to work on
                r, g, b = pixels[j, k]

                # altering the value of each pixel by a percent and then back to an int
                r = min(int(r * darken * red), 255)
                g = min(int(g * darken * green), 255)
                b = min(int(b * darken * blue), 255)

                # Save pixel
                pixels[j, k] = (r, g, b)

        # Show the edited image so user can see if they want to change it again
        image.show()
    return pixels


# Wrapper of print and set_format
# @param s String message to print to terminal and gets user input
# @returns in String whatever the user typed
def get_input(s=""):
    return input(formats["white"] + s + "\t\u2192 ").strip()


# Folder to look for and save images to, must be in working directory
folder = "cse110_images"

# Get files located in folder
files = os.listdir(folder)
# String where I will put all the image files
filesList = f"{formats['green']}"

# For each file, test if its a .png or .jpg and if so add to the list
for i in range(len(files)):
    if files[i].endswith(".png") or files[i].endswith(".jpg"):
        filesList += f"{files[i]:20}"

    # Every 5th entry add a new line
    if (i + 1) % 5 == 0:
        filesList += "\n"

# Print the list of files with a header
print(f"{formats['white']}Here is a list of all Images found in {formats['green']}{folder}{formats['white']}:")
print(filesList)

# Get inputs for images to use and what to name the new image
backName = get_input("What would you like for the background? (include extension)").strip()
foreName = get_input("What would you like for the foreground? (include extension)").strip()
backdropPath = f"{folder}/{backName}"
foregroundPath = f"{folder}/{foreName}"
outPath = f"{folder}/" + get_input("What would you like to name the new image? (include extension)").strip()

# How tolerant of variance of the green backdrop the program should be
tolerance = float(get_input("How tolerant should it be? (as a decimal value 1=max, .4 recommended 0=no tolerance)")
                  .strip())

# Initialize variables
# Images
backdrop = Image.open(backdropPath)
foreground = Image.open(foregroundPath)
# Sizes
fw, fh = foreground.size
bw, bh = backdrop.size
# Pixels
backPixels = backdrop.load()
frontPixels = foreground.load()

# run shader, which will edit the whole image darkness/r/g/b values
backPixels = shader(backdrop, backPixels, backName)
frontPixels = shader(foreground, frontPixels, foreName)

# Image we will save to
outImage = Image.new("RGB", backdrop.size)
outPixels = outImage.load()

# Randomly sample the front image to determine bacground color, then get the top 1 most common
mostCommon = sample(frontPixels, fw, fh).most_common(1)
# Collections returns result as [((r, g, b), occurrences)] so [0][0] is referring to the color itself
backgroundColor = mostCommon[0][0]

# For each pixel in the image
for x in range(bw-1):
    for y in range(bh-1):
        # Test if it is the background color within the leniency provided, if so then use the background pixel
        if is_background_color(frontPixels[x, y], leniency = tolerance):
            outPixels[x, y] = backPixels[x, y]
        else:
            # Otherwise, make a list of this pixel and all surrounding ones, checking that we aren't on an edge
            newPixels = [frontPixels[x, y]]
            if x > 0 and is_background_color(frontPixels[x - 1, y], leniency = tolerance):
                newPixels.append(backPixels[x - 1, y])
            if x < bw - 1 and is_background_color(frontPixels[x + 1, y], leniency = tolerance):
                newPixels.append(backPixels[x + 1, y])
            if y > 0 and is_background_color(frontPixels[x, y - 1], leniency = tolerance):
                newPixels.append(backPixels[x, y - 1])
            if x < bh - 1 and is_background_color(frontPixels[x, y + 1], leniency = tolerance):
                newPixels.append(backPixels[x, y + 1])

            # Blur the pixels in the list together, helps to remove residual green and make the image more seamless
            outPixels[x, y] = blur_rgb(newPixels)

# Save the image, and display that it has been saved. show completed image
outImage.save(outPath)
print(f"Saved image as: {formats['green']}{outPath}")
outImage.show()
