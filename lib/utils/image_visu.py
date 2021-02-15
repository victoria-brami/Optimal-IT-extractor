import scipy.io as sio
import cv2
import os.path as osp
import matplotlib.pyplot as plt
from lib.utils.misc import *


""" CONSTANT PARAMETERS """
NB_IMAGES = 11  # currently the number of images in an MRI sequence


# Load a single matlab image (in grey or in RGB colors)
def load_matlab_mri_image(path, gray_mode=False):
    im = sio.loadmat(path)
    if gray_mode:
        r, g, b = im['img'][:, :, 0], im['img'][:, :, 1], im['img'][:, :, 2]
        im['img'] = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return im['img'], im['img_hdr'][0]

# Load all the MRIs from the same patient and splits them into a list of images
def load_patient_mri_images(path, patient_id):
    image_path = osp.join(path, str(patient_id), 'data.mat')
    im, im_header = load_matlab_mri_image(image_path, gray_mode=False)
    images = []
    headers = []
    for image_idx in range(NB_IMAGES):
        images.append(im[:, :, image_idx])
        headers.append(im_header[image_idx])
    return images, headers, patient_id

def load_patient_mri_images_bis(path, patient_id):
    image_path = osp.join(path, str(patient_id), 'data.mat')
    im, im_header = load_matlab_mri_image(image_path, gray_mode=False)
    images = []
    headers = []
    for image_idx in range(NB_IMAGES):
        images.append(im[:, :, image_idx])
        headers.append(im_header[image_idx])
    return images, headers, patient_id

# Display the image (color mode or not)
def display_image(im):
    cv2.imshow('image', im)

# Save the image
def save_my_histogram_figure(root_dir, patient_id, timestamp):
    if not osp.isdir(osp.join(root_dir, patient_id)):
        os.mkdir(osp.join(root_dir, patient_id))
    plt.savefig(osp.join(root_dir, patient_id, timestamp))

# Display the histogram of colors
def display_color_histogram(ims, headers, patient_id, root_dir):

    # Create directory is it does not exist
    if not osp.isdir(root_dir):
        os.mkdir(root_dir)

    for j in range(NB_IMAGES):
        fig, ax = plt.subplots(2, 1)
        hist1 = cv2.calcHist([ims[j]], [0], None, [256], [0, 256])
        ax[0].imshow(ims[j], cmap='gray')
        ax[1].plot(hist1)
        ax[0].set_title(headers[j][0])

        # Save figures
        fig_name = 'TI_{}_ms'.format(headers[j][0].split()[-1])
        save_my_histogram_figure(root_dir, patient_id, fig_name)
        close_my_figure()
        #plt.show()


# Main function
def generate_histogram_per_patient():

    # identify patient ids
    ROOT_HISTO = '../../data/BlackBlood'
    ROOT = '../../data/TIScoutBlackBlood'
    patient_ids = patient_id_extractor(ROOT)
    print('Patient ids', patient_ids)
    for patient_id in patient_ids[-7:]:
        print('PATIENT {}'.format(patient_id))
        images, headers, patient_id = load_patient_mri_images(ROOT, patient_id)
        display_color_histogram(images, headers, patient_id, osp.join(ROOT_HISTO, 'histograms'))
        print()


if __name__ == '__main__':
    generate_histogram_per_patient()
    print('Great, everything is fine !')