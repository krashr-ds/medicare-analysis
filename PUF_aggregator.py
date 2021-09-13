import utils
import re
import pandas as pd

# SSA2FIPS = utils.load_data("data", "ssa_fips_state_county2011_augmented.csv")
# BRFSS = utils.load_data("data", "BRFSSCountyAggregates2010.csv")
# PUF = utils.load_data("data/PUF", "PUF_COUNTY_SUMMARY.csv")
# PUF2 = utils.load_data("data/PUF", "PUF_COUNTY_SUMMARY_50.csv")
PUF = utils.load_data("data/PUF", "PUF_ELIX_IP2009.csv")
RWJF = utils.load_data("data", "RWJF2010.csv")

# Only Need CBSA Info from SSA2FIPS
# SSA2FIPS.drop(["BENE_COUNTY_CD", "FULL_FIPS_CODE", "SP_STATE_CODE"], axis=1, inplace=True)

# Rename RWJF Columns
RWJF.columns = ["FIPS", "STATE", "COUNTY", "NUM_COUNTIES", "HO_RANK", "HO_PROP_RANK", "HO_QUARTILE", "HF_RANK", "HF_PROP_RANK", "HF_QUARTILE"]

# Split FIPS field in RWJF into State Code and County Code
match_fips = re.compile(r"^(\d{1,2})(\d{3})$")

RWJF["FIPS"] = RWJF["FIPS"].astype(str)
RWJF["StateCode"] = RWJF["FIPS"].replace(to_replace=match_fips, value=r"\1", regex=True).astype("float")
RWJF["CountyFIPS"] = RWJF["FIPS"].replace(to_replace=match_fips, value=r"\2", regex=True).astype("float")

# Join CBSA Information into PUF Data
# PUF_FIPS = pd.merge(PUF, SSA2FIPS, on=["FIPS_STATE_CODE", "FIPS_COUNTY_CODE"], how='left')
# PUF2_FIPS = pd.merge(PUF2, SSA2FIPS, on=["FIPS_STATE_CODE", "FIPS_COUNTY_CODE"], how='left')

# Join in RWJF Rankings
PUF_RWJF = pd.merge(PUF, RWJF, left_on=["FIPS_STATE_CODE", "FIPS_COUNTY_CODE"], right_on=["StateCode", "CountyFIPS"], how='left')
# PUF2_RWJF = pd.merge(PUF2_FIPS, RWJF, left_on=["FIPS_STATE_CODE", "FIPS_COUNTY_CODE"], right_on=["StateCode", "CountyFIPS"], how='left')

# Finally, join in the BRFSS data for the 302 counties that have it.
# PUF_BRFSS = pd.merge(PUF_RWJF, BRFSS, left_on=["FIPS_STATE_CODE", "FIPS_COUNTY_CODE"], right_on=["StateCode", "CountyFIPS"], how='left')
# PUF2_BRFSS = pd.merge(PUF2_RWJF, BRFSS, left_on=["FIPS_STATE_CODE", "FIPS_COUNTY_CODE"], right_on=["StateCode", "CountyFIPS"], how='left')

# Write to CSV
# PUF_RWJF.to_csv("data/PUF/PUF_RWJF_MERGED.csv")
PUF_RWJF.to_csv("data/PUF/PUF_RWJF_IP2009.csv")
# PUF2_BRFSS.to_csv("data/PUF/PUF_BRFSS_MERGED_50.csv")