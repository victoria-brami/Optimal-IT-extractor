import os
from project_config import *

# create data directory
if not os.path.exists(cfg.ROOT):
    os.mkdir(cfg.ROOT)

# install all the packages
os.system('pip3 install pandas')
os.system('pip3 install numpy')
os.system('pip3 install scipy')
os.system('pip3 install pathlib')
os.system('pip3 install torch')
os.system('pip3 install cv2')
os.system('pip3 install PyQt5')
os.system('pip3 install matplotlib')
os.system('pip3 install argparse')
