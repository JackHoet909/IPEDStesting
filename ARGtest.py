import argparse
import pandas as p
from pathlib import Path


def read_and_label(path, label):

    #Reads the CSV file that we are using (LATIN1 is the encoding standard because IPEDS data tends to feature Western European characters)
    df = p.read_csv(path, encoding="latin1")

    #Puts the file in a dataframe
    label_column = p.DataFrame(df)

    #Adds a column to the far left side of the file
    #Header is FILENAME and the data is the name of our file (which is stretched to the bottom row)
    label_column.insert(0, 'FILENAME', label)

    return label_column

# Set up argument parser
parser = argparse.ArgumentParser(description="Concatenate multiple CSV files into one and add filename labels.")
parser.add_argument("CSVfiles", nargs="+", help="Concatenating multiple CSV files into one file") #Allows one or more files to be passed
parser.add_argument("--output", default="UntitledMergedCSVFile.csv", help="Output CSV file name") #Sets up a default output name if not explicitly called
args = parser.parse_args() #Parse the arguments when used in the command line


#For each CSV file given, read its name (no folder but with .csv extension) and label an extra column using just the filename (no folder and .csv extension)
data_frames = [read_and_label(Path(path).name, Path(path).stem) for path in args.CSVfiles]

#Put the files all next to each other (from left to right)
merged_data_frame = p.concat(data_frames, axis=1)


#Run the command: Python ARGtest.py (insert file 1).csv (insert file 2).csv --output (insert new name).csv
print(merged_data_frame)

#Save it to a new CSV 
merged_data_frame.to_csv(args.output, index=False)