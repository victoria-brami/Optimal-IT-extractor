import os.path as osp


class Config:
    PATH_TO_PROJECT = '/Users/victoria.brami/Documents/Optimal-IT-extractor'

    # Root to TI Scout sequences database
    ROOT = osp.join(PATH_TO_PROJECT, 'data', 'TIScoutBlackBlood')

    # Number of image in each measured
    NB_IMAGES_PER_MRI_SEQUENCE = 11

    # Csv Paths for TI Scout labels
    LABELS_CSV_PATH = osp.join(PATH_TO_PROJECT, 'data', 'labels.csv')


cfg = Config()