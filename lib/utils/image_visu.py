import scipy.io as sio
import cv2
import os
import os.path as osp
import matplotlib.pyplot as plt
from lib.utils.misc import *

NB_IMAGES = 11


# Load a single matlab image (in grey or in RGB colors)
def load_matlab_mri_image(path, gray_mode=False):
    im = sio.loadmat(path)
    if gray_mode:
        r, g, b = im['img'][:, :, 0], im['img'][:, :, 1], im['img'][:, :, 2]
        im['img'] = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return im['img']

# Load all the MRIs from the same patient
def load_patient_mri_images(path, patient_id):
    image_path = osp.join(path, str(patient_id), 'data.mat')
    im = load_matlab_mri_image(image_path, gray_mode=False)
    images = []
    for image in range(NB_IMAGES):
        images.append(im[:, :, image])
        print('Shape', type(im[:, :, image]))
    return images, patient_id

# Display the image (color mode or not)
def display_image(im):
    cv2.imshow('image', im)

# Save the image
def save_my_histogram_figure(root_dir, patient_id, timestamp):
    if not osp.isdir(osp.join(root_dir, patient_id)):
        os.mkdir(osp.join(root_dir, patient_id))
    plt.savefig(osp.join(root_dir, patient_id, timestamp, '.jpg'))




# Display the histogram of colors
def display_color_histogram(ims, patient_id, root_dir):

    print('ims', len(ims[0]))

    for j in range(NB_IMAGES):
        fig, ax = plt.subplots(2, 1)
        print(type(ims[j]))
        hist1 = cv2.calcHist([ims[j]], [0], None, [256], [0, 256])
        print(type(ims[j]))
        ax[0].imshow(ims[j], cmap='gray')
        ax[1].plot(hist1)
        ax[0].set_title('Instant {}'.format(j))
        save_my_histogram_figure(root_dir, patient_id, j)
        plt.show()


# Main function
def generate_histogram_per_patient():

    # identify patient ids
    ROOT = '../../data/TIScoutBlackBlood'
    patient_ids = patient_id_extractor(ROOT)
    for patient_id in patient_ids:
        images = load_patient_mri_images(ROOT, patient_id)
        display_color_histogram(images, patient_id, osp.join(ROOT, 'histograms'))


if __name__ == '__main__':
    generate_histogram_per_patient()


    print('Great, everything is fine !')