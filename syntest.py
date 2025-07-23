import pandas as p
import argparse
from pathlib import Path

def read_first_file(path):

    #Reads the CSV file that we are using (LATIN1 is the encoding standard because IPEDS data tends to feature Western European characters)
    df = p.read_csv(path, encoding="latin1", low_memory=False)

    return df

def read_second_file(path):

    #Reads the CSV file that we are using (LATIN1 is the encoding standard because IPEDS data tends to feature Western European characters)
    df = p.read_csv(path, encoding="latin1", low_memory=False)

    return df


parser = argparse.ArgumentParser(description="Synchronize and sort multiple CSV files into one.")
parser.add_argument("firstfile", help="This is the first file to align")
parser.add_argument("secondfile", help="This is the second file to align")
parser.add_argument("--output1", default="UntitledMergedCSVFile1.csv", help="Output CSV file name1") #Sets up a default output name if not explicitly called
args = parser.parse_args() #Parse the arguments when used in the command line


first_df = read_first_file(Path(args.firstfile)) #this file needs to have more data than the second file
second_df = read_second_file(Path(args.secondfile))

reindexed_df = second_df.reindex(columns=first_df.columns) #Checks to see if the second dataframe has the same columns as the first dataframe
#If not, the result will be blank for the new columns added

print(reindexed_df)

reindexed_df.to_csv(args.output1, index=False)

