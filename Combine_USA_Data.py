import pandas as pd 

# Sets the path for where raw data files are located.
# This location should contain each of the three folders for 
# both sexes, male, and female data, and each of these three 
# folders should contain 20 raw files from each of the 20 years.
path = "/Users/Andrew/Desktop/BMI706_Project"

# note that the outputed csv file will be created in the 
# same directory as this python file.

# Reads in the first cirrhosis data file
Cirrhosis_data = pd.read_csv(path + "/IHME_USA_CIRRHOSIS_COUNTY_RACE_ETHN_2000_2019_BOTH/IHME_USA_CIRRHOSIS_COUNTY_RACE_ETHN_2000_2019_MX_2000_BOTH_Y2024M06D20.CSV")

# Initializes the combined USA data file based on the first cirrhosis file
# And filters to just overall USA data
# Visual inspection of the data set shows that the overall USA data corresponds
# to the first 126 rows in each raw file.
# Credit to https://stackoverflow.com/questions/12021754/how-to-slice-a-pandas-dataframe-by-position
# for help with the following line.
USA_data = Cirrhosis_data[:126]
Combined_USA_data = USA_data


# Loops through each cirrhosis file from BOTH SEXES and adds it to the combined
# data. 
# Credit to https://www.w3schools.com/python/python_for_loops.asp
# for help with the following line.
for i in range(2001, 2020):
    Cirrhosis_data = pd.read_csv(path + "/IHME_USA_CIRRHOSIS_COUNTY_RACE_ETHN_2000_2019_BOTH/IHME_USA_CIRRHOSIS_COUNTY_RACE_ETHN_2000_2019_MX_" + str(i) + "_BOTH_Y2024M06D20.CSV")
    USA_data = Cirrhosis_data[:126]

    # Credit to https://pandas.pydata.org/docs/user_guide/merging.html
    # for help with the following line.
    Combined_USA_data = pd.concat([Combined_USA_data, USA_data], ignore_index=True)


# Loops through each cirrhosis file from FEMALES and adds it to the combined data. 
# Credit to https://www.w3schools.com/python/python_for_loops.asp
# for help with the following line.
for i in range(2000, 2020):
    Cirrhosis_data = pd.read_csv(path + "/IHME_USA_CIRRHOSIS_COUNTY_RACE_ETHN_2000_2019_FEMALE/IHME_USA_CIRRHOSIS_COUNTY_RACE_ETHN_2000_2019_MX_" + str(i) + "_FEMALE_Y2024M06D20.CSV")
    USA_data = Cirrhosis_data[:126]

    # Credit to https://pandas.pydata.org/docs/user_guide/merging.html
    # for help with the following line.
    Combined_USA_data = pd.concat([Combined_USA_data, USA_data], ignore_index=True)


# Loops through each cirrhosis file from MALES and adds it to the combined data. 
# Credit to https://www.w3schools.com/python/python_for_loops.asp
# for help with the following line.
for i in range(2000, 2020):
    Cirrhosis_data = pd.read_csv(path + "/IHME_USA_CIRRHOSIS_COUNTY_RACE_ETHN_2000_2019_MALE/IHME_USA_CIRRHOSIS_COUNTY_RACE_ETHN_2000_2019_MX_" + str(i) + "_MALE_Y2024M06D20.CSV")
    USA_data = Cirrhosis_data[:126]

    # Credit to https://pandas.pydata.org/docs/user_guide/merging.html
    # for help with the following line.
    Combined_USA_data = pd.concat([Combined_USA_data, USA_data], ignore_index=True)


# Writes the combined data file to a csv
# Credit to https://www.datacamp.com/tutorial/save-as-csv-pandas-dataframe
# for helping with this line.
Combined_USA_data.to_csv("Combined_USA_Data.csv")