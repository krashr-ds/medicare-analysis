import utils
import pandas as pd

years = [2008, 2009, 2010]
SSA2FIPS = utils.load_data("data", "ssa_fips_state_county2011_augmented.csv")

for y in years:
    f_name = str(y) + "BSF11.csv"
    PUF = utils.load_data("data/PUF", f_name)
    PUF.set_index("DESYNPUF_ID")

    PUF_fips = pd.merge(PUF, SSA2FIPS, on=['SP_STATE_CODE', 'BENE_COUNTY_CD'], how='left')
    outfile_name = "data/PUF/BSF_FIPS" + str(y) + ".csv"
    PUF_fips.to_csv(outfile_name)

print("All years written.\n")

dframe = {}
dframe["inpatient"] = pd.read_csv("data/PUF/20082010INPATIENT.csv")
dframe["inpatient"]["CLAIM_TYPE"] = "INPATIENT"
dframe["outpatient"] = pd.read_csv("data/PUF/20082010OUTPATIENT.csv")
dframe["outpatient"]["CLAIM_TYPE"] = "OUTPATIENT"

all_claims = pd.concat(dframe, 0)
all_claims["DESYNPUF_ID"].astype(str)
all_claims.set_index("DESYNPUF_ID")
all_claims.CLM_FROM_DT = pd.to_datetime(all_claims.CLM_FROM_DT, format="%Y%m%d")
all_claims.CLM_THRU_DT = pd.to_datetime(all_claims.CLM_THRU_DT, format="%Y%m%d")

df_full = {}
for y in years:
    f_name = "data/PUF/BSF_FIPS" + str(y) + ".csv"
    df = pd.read_csv(f_name)
    df.drop("Unnamed: 0", axis=1, inplace=True)
    df["DESYNPUF_ID"] = df["DESYNPUF_ID"].astype(str)
    df.set_index("DESYNPUF_ID")
    df.BENE_BIRTH_DT = pd.to_datetime(df.BENE_BIRTH_DT, format="%Y%m%d")
    df.BENE_DEATH_DT = pd.to_datetime(df.BENE_DEATH_DT, format="%Y%m%d")

    # select claims for the year
    start_string = str(y) + "0101"
    end_string = str(y) + "1231"
    start_date = pd.to_datetime(start_string, format="%Y%m%d")
    end_date = pd.to_datetime(end_string, format="%Y%m%d")
    claims_df_yr = all_claims.loc[
        (all_claims['CLM_THRU_DT'] > start_date) & (all_claims['CLM_THRU_DT'] < end_date)]

    # join them in
    df_full[y] = pd.merge(df, claims_df_yr, how='left', on="DESYNPUF_ID")
    df_full[y].set_index("DESYNPUF_ID")

    # add beneficiary age and year, if possible
    if df_full[y]["CLM_THRU_DT"].notna:
        df_full[y]["BENE_AGE"] = round((df_full[y]["CLM_THRU_DT"] - df_full[y]["BENE_BIRTH_DT"]).dt.days / 365.2425)
    df_full[y]["YEAR"] = y
    f_name = "data/PUF/IPANDOP_FIPS" + str(y) + ".csv"
    df_full[y].to_csv(f_name)

allyears = pd.concat(df_full, 0)
allyears.to_csv("data/PUF/IPANDOP_FIPS_ALL.csv")

print("All years written.\n")