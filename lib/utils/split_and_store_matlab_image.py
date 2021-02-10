from lib.utils.image_visu import load_patient_mri_images
from lib.utils.misc import *
import os.path as osp
import matplotlib.pyplot as plt

def split_and_save_new_image(root_dir, patient_id, destination_path=None):

    # Load the patient images
    im, im_header, patient_id = load_patient_mri_images(root_dir, patient_id)

    for image_index in range(len(im)):

        # Extract time of MRI acquisition for image name
        image_name = im_header[image_index][0].split()[-1]

        # Generate and save the image
        create_new_directory(destination_path, [patient_id])
        plt.imshow(im[image_index], cmap='gray_r')
        plt.imsave(osp.join(destination_path, patient_id, '{}.png'.format(image_name)), im[image_index])
        close_my_figure()

if __name__ == '__main__':
    ROOT = '../../data/TIScoutBlackBlood'
    DESTINATION = '../../data/TIScoutBlackBlood_split'
    patient_ids = patient_id_extractor(ROOT)
    for patient in patient_ids:
        split_and_save_new_image(ROOT, patient, destination_path=DESTINATION)
