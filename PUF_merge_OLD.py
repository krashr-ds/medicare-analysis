import manip
import pandas as pd
import datetime as dt

years = [2008, 2009, 2010]
cities = ["MIAMI", "PHOENIX", "DALLAS", "RIVERSIDE", "SANBERNARDINO", "DETROIT"]
inpatient_df = pd.read_csv("data/PUF/20082010INPATIENT.csv")
inpatient_df["DESYNPUF_ID"] = inpatient_df["DESYNPUF_ID"].astype(str)
inpatient_df.set_index("DESYNPUF_ID")
inpatient_df.CLM_THRU_DT=pd.to_datetime(inpatient_df.CLM_THRU_DT, format="%Y%m%d")

for c in cities:
    for y in years:
        f_name = "data/PUF/" + c + "_BSF" + str(y) + ".csv"
        df = pd.read_csv(f_name)
        df.drop("Unnamed: 0", axis=1, inplace=True)
        df["DESYNPUF_ID"] = df["DESYNPUF_ID"].astype(str)
        df.set_index("DESYNPUF_ID")
        df.BENE_BIRTH_DT=pd.to_datetime(df.BENE_BIRTH_DT, format="%Y%m%d")

        #select inpatient claims for the year
        start_string = str(y) + "0101"
        end_string = str(y) + "1231"
        start_date = pd.to_datetime(start_string, format="%Y%m%d")
        end_date = pd.to_datetime(end_string, format="%Y%m%d")
        inpatient_df_sub = inpatient_df.loc[(inpatient_df['CLM_THRU_DT'] > start_date) & (inpatient_df['CLM_THRU_DT'] < end_date)]
        inpatient_df_sub["DESYNPUF_ID"] = inpatient_df_sub["DESYNPUF_ID"].astype(str)
        inpatient_df_sub.set_index("DESYNPUF_ID")
        #join them in
        df_full = pd.merge(df, inpatient_df_sub, how='left', on="DESYNPUF_ID")
        df_full.set_index("DESYNPUF_ID")

        #add beneficiary age and year
        df_full["BENE_AGE"] = round((df_full["CLM_THRU_DT"] - df_full["BENE_BIRTH_DT"]).dt.days / 365.2425)
        df_full["YEAR"] = y
        f_name2 = "data/PUF/" + c + "_IPF" + str(y) + ".csv"
        df_full.to_csv(f_name2)


#stack augmented dataframes
for c in cities:
    f1 = "data/PUF/" + c + "_IPF2008.csv"
    f2 = "data/PUF/" + c + "_IPF2009.csv"
    f3 = "data/PUF/" + c + "_IPF2010.csv"
    c_stack = manip.stack_dataframes([f1, f2, f3], "YEAR", "[0-9]+", orientation=0, add_index=0)
    c_stack.set_index("DESYNPUF_ID")
    stacked_file = "data/PUF/" + c + "_IPF20082010.csv"
    c_stack.to_csv(stacked_file)

#stack county-types for easy comparisons
dframe = {}
dframe["data/PUF/MIAMI_IPF20082010.csv"] = pd.read_csv("data/PUF/MIAMI_IPF20082010.csv")
dframe["data/PUF/PHOENIX_IPF20082010.csv"] = pd.read_csv("data/PUF/PHOENIX_IPF20082010.csv")
high_counties = pd.concat(dframe, 0)

dframe2 = {}
dframe2["data/PUF/DALLAS_IPF20082010.csv"] = pd.read_csv("data/PUF/DALLAS_IPF20082010.csv")
dframe2["data/PUF/RIVERSIDE_IPF20082010.csv"] = pd.read_csv("data/PUF/RIVERSIDE_IPF20082010.csv")
medium_counties = pd.concat(dframe2, 0)

dframe3 = {}
dframe3["data/PUF/SANBERNARDINO_IPF20082010.csv"] = pd.read_csv("data/PUF/SANBERNARDINO_IPF20082010.csv")
dframe3["data/PUF/DETROIT_IPF20082010.csv"] = pd.read_csv("data/PUF/DETROIT_IPF20082010.csv")
low_counties = pd.concat(dframe3, 0)

all_counties = pd.concat([high_counties, medium_counties, low_counties], 0)

high_counties.to_csv("data/PUF/HIGH_IPF20082010.csv")
medium_counties.to_csv("data/PUF/MEDIUM_IPF20082010.csv")
low_counties.to_csv("data/PUF/LOW_IPF20082010.csv")
all_counties.to_csv("data/PUF/ALL_IPF20082010.csv")
