import manip
import re
import numpy as np
import pandas as pd

brfss_2010 = pd.read_sas("/home/kylier/python/DS/data/CNTY10.xpt")

# Strip garbage out of SAS-formatted fields
fields_to_clean = ["_CNTYNAM", "IDATE", "IMONTH", "IDAY", "IYEAR", "INTVID"]
clean_middle_re = re.compile(r"^\s*b[\'|`]([^\'|`]+)[\'|`]\s*$")

for f in fields_to_clean:
    brfss_2010[f] = brfss_2010[f].astype(str)
    brfss_2010[f] = brfss_2010[f].replace(to_replace=clean_middle_re, value=r"\1", regex=True)

# Create DataFrame with Columns of Interest
big_df = pd.DataFrame(brfss_2010,
                      columns=["_STATE", "_CNTYNAM", "_CNTY", "ADJCNTY",        # LOCATION: State, County Name, County FIPS, County Weight
                               "GENHLTH", "PHYSHLTH", "MENTHLTH",               # QOL: General Health Rating, Days in Poor Physical Health, Days in Poor Mental Health,
                               "HLTHPLAN", "MEDCOST", "CHECKUP1",               # ACCESS: Health Insurance, Care Cost Prohibitive?, How Long Since Last Check-up?
                               "QLREST2", "EXERANY2",                           # LIFESTYLE: Quality of Rest/Sleep, Leisure-time Exercise
                               "_DRNKDY3", "_RFSEAT3", "_RFSMOK3", "_BMI4",     # Drinking, Seatbelt Use, Smoking, BMI
                               "DIABETE2",                                      # COMORBIDITIES (Binary): Diabetes
                               "CVDINFR4", "CVDCRHD4",                          # MI, Angina or CVD
                               "CVDSTRK3",                                      # Stroke
                               "ASTHMA2",                                       # Asthma
                               "ADDEPEV", "ADANXEV",                            # Depression, Anxiety
                               "CNCRHAVE",                                      # Cancer
                               "QLACTLM2",                                      # Disability
                               "AGE", "_AGEG5YR", "RACE2", "SEX"])              # DEMOGRAPHICS: Age (continuous), Age Group, Race, Sex


# Re-name Columns to Understandable Names
big_df.columns = ["StateCode", "CountyName", "CountyFIPS", "CountyWeight",
                  "GeneralHealth", "PhysHealthDays", "MentHealthDays",
                  "HealthIns", "CostTooHigh", "LastCheckup",
                  "NotEnoughRestDays", "LeisureExercise",
                  "DrinksPerDay", "Seatbelt", "Smoker", "BMI",
                  "Diabetes",
                  "MI", "AnginaCVD",
                  "Stroke",
                  "Asthma",
                  "Depression", "Anxiety",
                  "Cancer",
                  "Disability",
                  "Age", "AgeGroup", "Race", "Sex"]

# Create binary summary variable BinaryRace, based on Race
# 0 = white (about 80% of the population), 1 = another primary racial or ethnic identity
manip.create_binary(big_df, ["Race"], [1], [2, 3, 4, 5, 6], "BinaryRace", [0, 1])

# Change Sex 1, 2 to Sex 1, 0
# 0 = Female, 1 = Male, Other = NaN / NULL
manip.create_binary(big_df, ["Sex"], [1], [2], "Sex")
big_df["Sex"].replace(7, np.nan, inplace=True)
big_df["Sex"].replace(9, np.nan, inplace=True)


# Create Label Columns

# Create new column with State Names
states_dict = {1: 'Alabama', 2: 'Alaska', 4: 'Arizona', 5: 'Arkansas', 6: 'California', 8: 'Colorado', 9: 'Connecticut',
               10: 'Delaware', 11: 'District of Columbia', 12: 'Florida', 13: 'Georgia', 15: 'Hawaii', 16: 'Idaho',
               17: 'Illinois', 18: 'Indiana', 19: 'Iowa', 20: 'Kansas', 21: 'Kentucky', 22: 'Louisiana', 23: 'Maine',
               24: 'Maryland', 25: 'Massachusetts', 26: 'Michigan', 27: 'Minnesota', 28: 'Mississippi', 29: 'Missouri',
               30: 'Montana', 31: 'Nebraska', 32: 'Nevada', 33: 'New Hampshire', 34: 'New Jersey', 35: 'New Mexico',
               36: 'New York', 37: 'North Carolina', 38: 'North Dakota', 39: 'Ohio', 40: 'Oklahoma', 41: 'Oregon',
               42: 'Pennsylvania', 44: 'Rhode Island', 45: 'South Carolina', 46: 'South Dakota', 47: 'Tennessee',
               48: 'Texas', 49: 'Utah', 50: 'Vermont', 51: 'Virginia', 53: 'Washington', 54: 'West Virginia',
               55: 'Wisconsin', 56: 'Wyoming', 66: 'Guam', 72: 'Puerto Rico', 78: 'Virgin Islands'}

manip.recode_col(big_df, "StateCode", states_dict, "StateName")

states_abbr_dict = {1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE', 11: 'DC', 12: 'FL',
                    13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA', 20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME',
                    24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN', 28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE', 32: 'NV', 33: 'NH',
                    34: 'NJ', 35: 'NM', 36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI',
                    45: 'SC', 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA', 54: 'WV',
                    55: 'WI', 56: 'WY', 66: 'GU', 72: 'PR', 78: 'VI'}

manip.recode_col(big_df, "StateCode", states_abbr_dict, "StateAbbreviation")

# Collapse AgeGroup variable into one more similar to DeSYNPuf
age_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
            10: 1, 11: 2, 12: 2, 13: 3, 14: np.nan}
age_dict2 = {0: "lt 65", 1: "65-69", 2: "70-79", 3: "80+"}

manip.recode_col(big_df, "AgeGroup", age_dict, "AgeGroup")
manip.recode_col(big_df, "AgeGroup", age_dict2, "AgeGroupLabels")

sex_dict = {1: "Male", 0: "Female"}
manip.recode_col(big_df, "Sex", sex_dict, "SexLabels")

race_dict = {1: 0, 2: 1, 3: 3, 4: 3, 5: 4, 6: 6, 7: 5, 8: 2, 9: np.nan}
race_dict2 = {0: "white", 1: "Black", 3: "Asian/NH/PI", 4: "AI/AK Native", 6: "Other", 5: "Multi", 2: "Hispanic"}

manip.recode_col(big_df, "Race", race_dict, "Race")
manip.recode_col(big_df, "Race", race_dict2, "RaceLabels")


checkup_dict = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 8: 0, 9: np.nan}
checkup_dict2 = {5: "In past year", 4: "In past 2 years", 3: "In past 3 years", 2: "In past 5 years",
                 1: "More than 5 years ago", 0: "Never"}

manip.recode_col(big_df, "LastCheckup", checkup_dict, "LastCheckup")
manip.recode_col(big_df, "LastCheckup", checkup_dict2, "LastCheckupLabels")

recode_to_dummy = ["HealthIns", "CostTooHigh", "LeisureExercise", "Diabetes", "MI", "AnginaCVD",
                   "Stroke", "Asthma", "Depression", "Anxiety", "Cancer", "Disability", "Seatbelt",
                   "Smoker"]
for r in recode_to_dummy:
    if r == "Smoker":
        manip.create_binary(big_df, ["Smoker"], [1], [2], "Smoker", [0, 1])
    else:
        manip.create_binary(big_df, [r], [1], [2], r)

# Create a binary variable to reflect obesity
big_df["Obese"] = [1 if s > 30 else 0 for s in big_df["BMI"]]

# Set NaN Values

recode_9_to_NaNs = ["GeneralHealth", "HealthIns", "CostTooHigh", "LeisureExercise", "Diabetes", "MI", "AnginaCVD",
                    "Stroke", "Asthma", "Depression", "Anxiety", "Cancer", "Disability", "Seatbelt", "Smoker"]
for c in recode_9_to_NaNs:
    big_df[c].replace(6, np.nan, inplace=True)
    big_df[c].replace(7, np.nan, inplace=True)
    big_df[c].replace(8, np.nan, inplace=True)
    big_df[c].replace(9, np.nan, inplace=True)

big_df["BMI"].replace(9999, np.nan, inplace=True)
big_df["DrinksPerDay"].replace(9900, np.nan, inplace=True)

for dc in ["PhysHealthDays", "MentHealthDays", "NotEnoughRestDays"]:
    big_df[dc].replace(88, 0, inplace=True)


# create CSV of clean DataFrame
#
big_df.to_csv("data/BRFSSCountyData2010.csv")

# I was going to trim this down to only those over 65, or those who are disabled,
# but I decided to keep everyone. The at risk now are the sick tomorrow!
df_copy = big_df.copy()


def computeWeightedMeans(x):
    means_dict = {"GeneralHealthWMean": 'GeneralHealth',
                  "PhysHealthDaysWMean": 'PhysHealthDays',
                  "MentHealthDaysWMean": 'MentHealthDays',
                  "HealthInsWMean": 'HealthIns',
                  "CostTooHighWMean": 'CostTooHigh',
                  "LastCheckupWMean": 'LastCheckup',
                  "NotEnoughRestDaysWMean": 'NotEnoughRestDays',
                  "LeisureExerciseWMean": 'LeisureExercise',
                  "DrinksPerDayWMean": 'DrinksPerDay',
                  "SeatbeltWMean": 'Seatbelt',
                  "SmokerWMean": 'Smoker',
                  "BMIWMean": 'BMI',
                  "DiabetesWMean": 'Diabetes',
                  "MIWMean": 'MI',
                  "AnginaCVDWMean": 'AnginaCVD',
                  'StrokeWMean': 'Stroke',
                  "AsthmaWMean": 'Asthma',
                  "DepressionWMean": 'Depression',
                  "AnxietyWMean": 'Anxiety',
                  "CancerWMean": 'Cancer',
                  "DisabilityWMean": 'Disability',
                  "AgeWMean": 'Age',
                  "SexWMean": 'Sex',
                  "BinaryRaceWMean": 'BinaryRace',
                  "ObeseWMean": 'Obese'}

    for key, value in means_dict.items():
        x[key] = x[value] / x[value].sum() * x["CountyWeight"]

    return x


CountyAggregate = df_copy.groupby(["StateCode", "CountyFIPS"]).apply(computeWeightedMeans)
CountyAggregate.drop(["CountyWeight", "GeneralHealth", "PhysHealthDays", "MentHealthDays", "BinaryRace", "Obese",
                        "HealthIns", "CostTooHigh", "LastCheckup", "NotEnoughRestDays", "LeisureExercise", "DrinksPerDay", "Seatbelt",
                        "Smoker", "BMI", "Diabetes", "MI", "AnginaCVD", "Stroke", "Asthma", "Depression", "Anxiety", "Cancer",
                        "Disability", "Age", "AgeGroup", "Race", "Sex", "StateAbbreviation",
                      "AgeGroupLabels", "SexLabels", "RaceLabels", "LastCheckupLabels"], axis=1, inplace=True)

CountyAggregate = CountyAggregate.groupby(["StateCode", "CountyFIPS"]).aggregate("mean")

# create CSV of County aggregates
#
CountyAggregate.to_csv("data/BRFSSCountyAggregates2010.csv")