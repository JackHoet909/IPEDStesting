import pandas as p
import argparse
from pathlib import Path

def read_file(path):

    #Reads the CSV file that we are using (LATIN1 is the encoding standard because IPEDS data tends to feature Western European characters)
    df = p.read_csv(path, encoding="latin1", low_memory=False)

    return df



parser = argparse.ArgumentParser(description="Switch the wide format of a CSV file to long format.")
parser.add_argument("firstfile", help="Input your file to be formatted.")
parser.add_argument("--output", default="UntitledFormattedCSVFile1.csv", help="Output CSV file name1") #Sets up a default output name if not explicitly called
args = parser.parse_args() #Parse the arguments when used in the command line


df = read_file(Path(args.firstfile)) #this file needs to have more data than the second file

df_long = p.melt(df, id_vars=["FILENAME", "UNITID"], var_name="Variable", value_name="Value")

print(df_long)

df_long.to_csv(args.output, index=False)