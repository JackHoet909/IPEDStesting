import pandas as p
import argparse
from pathlib import Path

def read_file(path):

    #Reads the CSV file that we are using (LATIN1 is the encoding standard because IPEDS data tends to feature Western European characters)
    df = p.read_csv(path, encoding="latin1", low_memory=False)

    return df


parser = argparse.ArgumentParser(description="Map the codevalues from your second table to their corresponding valuelabels from the first table")
parser.add_argument("mapping_file", help="CSV file containing code-to-label mapping (table1)")
parser.add_argument("data_file", help="CSV file containing codes to be mapped (table2)")
parser.add_argument("--output", default="UntitledMergedCSVFile1.csv", help="Output CSV file name1") #Sets up a default output name if not explicitly called
args = parser.parse_args() #Parse the arguments when used in the command line


table1 = read_file(Path(args.mapping_file))
table2 = read_file(Path(args.data_file))

# Create a dictionary from table1 for mapping
mapping_dict = table1.set_index('code')['label'].to_dict() #table 1 has code data and label data

# Map the code values in table2 to their corresponding labels
table2['label'] = table2['code'].map(mapping_dict) #table 2 has code data but no label data

print(table2)

table2.to_csv(args.output, index=False)