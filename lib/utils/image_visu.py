import scipy.io as sio
import cv2
import os
import os.path as osp
import matplotlib.pyplot as plt
import numpy as np

# Extract patients IDs
def patient_id_extractor(path):

    patient_ids = os.listdir(path)
    if '.DS_Store' in patient_ids:
        patient_ids.remove('.DS_Store')
    return patient_ids

# Splits a list of strings and resort them
def sort_my_strings_list(str_list):
    sorted_list = []
    for name in str_list:
        new_name = name.split('_')
        sorted_list.append([name, new_name[-1]])
    sorted_list = sorted(sorted_list[-1], key='int')
    return None


# Load a single matlab image (in grey or in RGB colors)
def load_matlab_mri_image(path, gray_mode=False):
    im = sio.loadmat(path)
    if gray_mode:
        r, g, b = im['img'][:, :, 0], im['img'][:, :, 1], im['img'][:, :, 2]
        im['img'] = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return im['img']

# Load all the MRIs from the same patient
def load_patient_mri_images(path, patient_id, gray_mode=False):
    root_path = osp.join(path, str(patient_id))
    images_folders = [name for name in os.listdir(osp.join(root_path, 'DICOMS'))]
    if '.DS_Store' in images_folders:
        images_folders.remove('.DS_Store')
    images = []
    for name in images_folders:
        image_path = osp.join(root_path, 'DICOMS', name, 'data.mat')
        im = load_matlab_mri_image(image_path, gray_mode=False)
        images.append(im)
    return images, images_folders

# Display the image (color mode or not)
def display_image(im):
    cv2.imshow('image', im)


# Display the histogram of colors
def display_color_histogram(ims, titles=None):
    nb_images = len(ims)
    print(titles)
    for j in range(len(ims) // 3):
        fig, ax = plt.subplots(2, 3)
        for i in range(3):
            hist1 = cv2.calcHist([ims[3 * j + i]], [0], None, [256], [0, 256])
            ax[0, i].imshow(ims[3 * j + i], cmap='gray')
            ax[1, i].plot(hist1)
            ax[0, i].set_title(titles[3 * j + i])
    # plt.show()


if __name__ == '__main__':
    ROOT = '../../data/BlackBlood/DICOMS_4Victoria/DICOMS_4Victoria'

    # identify patient ids
    patient_ids = patient_id_extractor(ROOT)

    # Display images and corresponding histograms
    images, images_folders = load_patient_mri_images(ROOT, '5', gray_mode=False)
    display_color_histogram(images, images_folders)

    print('Great, everything is fine !')