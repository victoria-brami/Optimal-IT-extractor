from torch.utils.data import Dataset
import pandas as pd

class TiScoutDataset(Dataset):

    def __init__(self, csv_name):

        self.csv_name = csv_name
        self.data = []

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return None

if __name__ == '__main__':
    print('Great, everything is fine !')

