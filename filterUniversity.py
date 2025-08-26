import pandas as p
import argparse
from pathlib import Path

def read_file(path):

    #Reads the CSV file that we are using (LATIN1 is the encoding standard because IPEDS data tends to feature Western European characters)
    df = p.read_csv(path, encoding="latin1", low_memory=False)

    return df


parser = argparse.ArgumentParser(description="Filtering a dataframe based off of their UserID")
parser.add_argument("fileName", help="Input the name of your file")
parser.add_argument("unitID", help="Put down the unit id of the university", type=int)
parser.add_argument("--output", default="UntitledMergedCSVFile1.csv", help="Output CSV file name1") #Sets up a default output name if not explicitly called
args = parser.parse_args() #Parse the arguments when used in the command line


original_df = read_file(Path(args.fileName)) #this file needs to have more data than the second file

filtered_df = original_df[original_df["UNITID"] == args.unitID] #Checks to see if the second dataframe has the same columns as the first dataframe
#If not, the result will be blank for the new columns added

print(filtered_df)

filtered_df.to_csv(args.output, index=False)