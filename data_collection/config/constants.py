import os 
from . import personal_constants as pc

SNA_DATA_ROOT = os.path.join(pc.GOOGLE_DRIVE_ROOT, 'SNA4DS', 'Data')
SBM_DATA_ROOT = os.path.join(pc.GOOGLE_DRIVE_ROOT, 'SBM', 'Data')

YOUTUBE_API_KEY = pc.YOUTUBE_API_KEY
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Will delete below later, made it as a test to see if the constants.py file works. Check yourself also.
# make dataframe of google data_first_sample.csv in SBMDATAROOT
# import pandas as pd
# df = pd.read_csv(os.path.join(SBMDATAROOT, 'google_data_first_sample.csv'))
# print(df.head())
