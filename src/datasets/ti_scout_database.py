from torch.utils.data import Dataset
import pandas as pd
from project_config import *

class TiScoutDataset(Dataset):

    def __init__(self, csv_name, transform=None):
        """ CSV contains"""
        self.csv_name = csv_name
        self.transform = transform


        self.data = self._load_data()
        self.set = self._build_net_inputs()


    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        """ Images will be loaded only at that moment in order to optimize complexity """
        return None

    def _load_data(self):
        data = []
        csv_contents = pd.read_csv(self.csv_name)
        print("csv", csv_contents)
        # Browse dataset row per row
        for patient_id, row in csv_contents.iterrows():
            data_contents = row[:].to_numpy()
            data.append(dict(patient_id=str(data_contents[0]), ti_scout=data_contents[1:]))
        return data

    def _build_net_inputs(self):
        """ must split the data into sequences of four images """
        set = []
        for data_item in self.data:
            # We can create (NB_IMAGES - 4 + 1 ) Sequences
            for batch_item in range(cfg.NB_IMAGES_PER_MRI_SEQUENCE - 4 + 1):
                new_batch = dict(patient_id=data_item['patient_id'],
                                 ti_scout_image_index = [j+1 for j in range(batch_item, batch_item+ 4)],
                                 ti_scout=data_item['ti_scout'][batch_item:batch_item+ 4])
                set.append(new_batch)
        return set

if __name__ == '__main__':
    ex = TiScoutDataset(cfg.LABELS_CSV_PATH)
    print('Great, everything is fine !')

