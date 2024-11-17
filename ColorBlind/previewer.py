import os

from tkinter import *

from PIL import Image, ImageTk
import numpy as np


folder_path = "./test_"  # replace with your directory


# get list of all files in directory

file_list = os.listdir(folder_path)

# filter out all non-image files

img_files = [file for file in file_list if file.endswith(('jpeg', 'jpg', 'png', 'JPG'))]
print(file_list)

index = 0  # index of the currently displayed picture

root = Tk()

# create a label which will display the image

label = Label(root)

label.grid(row=0, column=1)


def adapt2(im):
    # Convert the image to a NumPy array for fast processing
    arr = np.array(im, dtype=np.float32)  # Using float for calculations to prevent overflow

    # Extract RGB channels
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

    # Apply the first condition
    diff_rg = r - g
    mask_rg = diff_rg > 0
    r[mask_rg] = np.minimum(r[mask_rg] + diff_rg[mask_rg] * float(g2r_var.get()) / 2, 255)
    g[mask_rg] = np.maximum(g[mask_rg] - diff_rg[mask_rg] * float(g2r_var.get()) / 2, 0)

    mask_gr = ~mask_rg  # Opposite condition
    g[mask_gr] = np.minimum(g[mask_gr] + (-diff_rg[mask_gr]) * float(g2r_var.get()) / 2, 255)
    r[mask_gr] = np.maximum(r[mask_gr] - (-diff_rg[mask_gr]) * float(g2r_var.get()) / 2, 0)

    # Apply the second condition
    diff_gb = g - b
    mask_gb = diff_gb > 0
    g[mask_gb] = np.minimum(g[mask_gb] + diff_gb[mask_gb] * float(g2b_var.get()) / 2, 255)
    b[mask_gb] = np.maximum(b[mask_gb] - diff_gb[mask_gb] * float(g2b_var.get()) / 2, 0)

    mask_bg = ~mask_gb
    b[mask_bg] = np.minimum(b[mask_bg] + (-diff_gb[mask_bg]) * float(g2b_var.get()) / 2, 255)
    g[mask_bg] = np.maximum(g[mask_bg] - (-diff_gb[mask_bg]) * float(g2b_var.get()) / 2, 0)

    # Apply the third condition
    diff_rb = r - b
    mask_rb = diff_rb > 0
    r[mask_rb] = np.minimum(r[mask_rb] + diff_rb[mask_rb] * float(b2r_var.get()) / 2, 255)
    b[mask_rb] = np.maximum(b[mask_rb] - diff_rb[mask_rb] * float(b2r_var.get()) / 2, 0)

    mask_br = ~mask_rb
    b[mask_br] = np.minimum(b[mask_br] + (-diff_rb[mask_br]) * float(b2r_var.get()) / 2, 255)
    r[mask_br] = np.maximum(r[mask_br] - (-diff_rb[mask_br]) * float(b2r_var.get()) / 2, 0)

    # Reassemble the image
    arr[..., 0], arr[..., 1], arr[..., 2] = r, g, b

    # Convert back to uint8 and return as an image
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def adapt(im):
    # Load pixels
    pixels = im.load()
    # Iterate over each pixel
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            r, g, b = pixels[i, j]
            if r > g:
                r = min(int(r + (r - g) * float(g2r_var.get()) / 2), 255)
                g = max(int(g - (r - g) * float(g2r_var.get()) / 2), 0)
            else:
                g = min(int(g + (g - r) * float(g2r_var.get()) / 2), 255)
                r = max(int(r - (g - r) * float(g2r_var.get()) / 2), 0)
            if g > b:
                g = min(int(g + (g - b) * float(g2b_var.get()) / 2), 255)
                b = max(int(b - (g - b) * float(g2b_var.get()) / 2), 0)
            else:
                b = min(int(b + (b - g) * float(g2b_var.get()) / 2), 255)
                g = max(int(g - (b - g) * float(g2b_var.get()) / 2), 0)
            if r > b:
                r = min(int(r + (r - b) * float(b2r_var.get()) / 2), 255)
                b = max(int(b - (r - b) * float(b2r_var.get()) / 2), 0)
            else:
                b = min(int(b + (b - r) * float(b2r_var.get()) / 2), 255)
                r = max(int(r - (b - r) * float(b2r_var.get()) / 2), 0)
            # Set the red component to zero
            # r = min((r + 50), 255)
            pixels[i, j] = (r, g, b)


def show_image():

    global index, img_files, root, label

    img_path = os.path.join(folder_path, img_files[index])

    img = Image.open(img_path)
    # adapt(img)
    img = adapt2(img)
    tk_img = ImageTk.PhotoImage(img)

    label['image'] = tk_img

    label.photo = tk_img  # keep a reference to avoid garbage collection


def next_image():

    global index, img_files

    index = (index + 1) % len(img_files)  # prevent index from going out of bounds

    show_image()


def prev_image():

    global index, img_files

    index = (index - 1) % len(img_files)  # prevent index from going out of bounds

    show_image()


f = Frame(root)
f.grid(row=0, column=0)


g2r_var = StringVar()
g2r_var.set('')
g2r_entry = Spinbox(f, from_=0, to=2, values=[str(x / 10.0) for x in range(0, 21, 2)], command=show_image, textvariable=g2r_var)
g2r_entry.grid(row=0, column=0)
g2r_label = Label(f, text="green to red factor")
g2r_label.grid(row=0, column=1)

g2b_var = StringVar()
g2b_var.set('')
g2b_entry = Spinbox(f, from_=0, to=2, values=[str(x / 10.0) for x in range(0, 21, 2)], command=show_image, textvariable=g2b_var)
g2b_entry.grid(row=1, column=0)
g2b_label = Label(f, text="green to blue factor")
g2b_label.grid(row=1, column=1)

b2r_var = StringVar()
b2r_var.set('')
b2r_entry = Spinbox(f, from_=0, to=2, values=[str(x / 10.0) for x in range(0, 21, 2)], command=show_image, textvariable=b2r_var)
b2r_entry.grid(row=2, column=0)
b2r_label = Label(f, text="blue to red factor")
b2r_label.grid(row=2, column=1)


image_button_frame = Frame(f)
image_button_frame.grid(row=3, column=0)
button = Button(image_button_frame, text="Next Image", command=next_image)
button.grid(row=1, column=0)
prev_button = Button(image_button_frame, text="Prev Image", command=prev_image)
prev_button.grid(row=1, column=1)

show_image()  # show first image


root.mainloop()
