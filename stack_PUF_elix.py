import utils
import re
import pandas as pd

# Stack DataFrames
# files_list = ["data/PUF/inandop_elx_part1.csv", "data/PUF/inandop_elx_part2.csv", "data/PUF/inandop_elx_part3.csv", "data/PUF/inandop_elx_part4.csv"]
# dframes = {}
# for f in files_list:
#    dframes[f] = pd.read_csv(f)

# elix_df = pd.concat(dframes, 0)
# elix_df.to_csv("data/PUF/IPANDOP_FIPS_ELIX_ALL.csv")

#print("All years written.\n")

# Read in stacked file
PUF_CLAIMS = utils.load_data("data/PUF", "IPANDOP_FIPS_ALL.csv")
PUF_ELIX = utils.load_data("data/PUF", "IPANDOP_FIPS_ELIX_ALL.csv")

# Join on DeSYNPuf ID and CLM_ID
