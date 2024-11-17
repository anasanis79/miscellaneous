from PIL import Image
import os


def remove_red(im):
    # Load pixels
    pixels = im.load()
    # Iterate over each pixel
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            r, g, b = pixels[i, j]
            if r > g:
                r = min(int(r + (r - g) * 2), 255)
            else:
                g = min(int(g + (g - r)), 255)
            # Set the red component to zero
            # r = min((r + 50), 255)
            pixels[i, j] = (r, g, b)


def process_files(directory_path):
    for dir_path, _, filenames in os.walk(directory_path):
        for filename in filenames:
            im = Image.open(os.path.join(dir_path, filename))
            remove_red(im)
            im.save(os.path.join(dir_path, "o"+filename))
            #  print(os.path.join(dir_path, filename))  # Or do whatever you want with the filename


process_files("./test")

# # Load the image
#
# im = Image.open('input1.jpg')
#
# # Remove the red component
#
# remove_red(im)
#
# # Save the new image
#
# im.save('output1.jpg')