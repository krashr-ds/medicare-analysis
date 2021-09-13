import utils
import pandas as pd

years = [2008, 2009, 2010]
cities = ["MIAMI", "PHOENIX", "DALLAS", "RIVERSIDE", "SANBERNARDINO", "DETROIT"]
SSA2FIPS = utils.load_data("data", "ssa_fips_state_county2011_augmented.csv")

for y in years:
    f_name = str(y) + "BSF11.csv"
    PUF = utils.load_data("data/PUF", f_name)
    PUF.set_index("DESYNPUF_ID")

    PUF_fips = pd.merge(PUF, SSA2FIPS, on=['SP_STATE_CODE','BENE_COUNTY_CD'], how='left')
    MIAMI = PUF_fips[(PUF_fips["SP_STATE_CODE"] == 10) & (PUF_fips["BENE_COUNTY_CD"] == 120)]
    PHOENIX = PUF_fips[(PUF_fips["SP_STATE_CODE"] == 3) & (PUF_fips["BENE_COUNTY_CD"] == 60)]
    DALLAS = PUF_fips[(PUF_fips["SP_STATE_CODE"] == 45) & (PUF_fips["BENE_COUNTY_CD"] == 390)]
    RIVERSIDE = PUF_fips[(PUF_fips["SP_STATE_CODE"] == 5) & (PUF_fips["BENE_COUNTY_CD"] == 430)]
    SANBERNARDINO = PUF_fips[(PUF_fips["SP_STATE_CODE"] == 5) & (PUF_fips["BENE_COUNTY_CD"] == 460)]
    DETROIT = PUF_fips[(PUF_fips["SP_STATE_CODE"] == 23) & (PUF_fips["BENE_COUNTY_CD"] == 810)]

    print("New dataframes created for", y, "\nTotal number of records\nMiami: ", MIAMI.shape[0], "\nPhoenix: ", PHOENIX.shape[0], "\nDallas: ", DALLAS.shape[0],
              "\nRiverside: ", RIVERSIDE.shape[0], "\nSan Bernardino: ", SANBERNARDINO.shape[0], "\nDetroit: ", DETROIT.shape[0])

    for c in cities:
        outfile_name = "data/PUF/" + c + "_BSF" + str(y) + ".csv"
        eval(c).to_csv(outfile_name)

    print("County-specific files for ", y, " written.\n")

print("All years written.\n")

