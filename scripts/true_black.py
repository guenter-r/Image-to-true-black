import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt


def true_black(path, file_name, threshold = 25):
    name = file_name
    im = Image.open(os.path.join(path, name))
    new = np.array(im)

    # start filtering
    filter = new[:,:] < int(threshold)
    new[:,:][filter] = 0

    name = name.split('.')[0]
    new_name = f'{name}_black.jpg'
    plt.imsave(os.path.join(path, new_name), new)
    return new_name