import os 
import personalConstants as pc

SNADATAROOT = os.path.join(pc.GOOGLEDRIVEROOT, 'SNA4DS', 'Data')
SBMDATAROOT = os.path.join(pc.GOOGLEDRIVEROOT, 'SBM', 'Data')

YOUTUBEAPIKEY = pc.YOUTUBEAPIKEY

# Will delete below later, made it as a test to see if the constants.py file works. Check yourself also.
# make dataframe of google data_first_sample.csv in SBMDATAROOT
# import pandas as pd
# df = pd.read_csv(os.path.join(SBMDATAROOT, 'google_data_first_sample.csv'))
# print(df.head())
