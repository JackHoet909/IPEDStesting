import argparse
import pandas as p
from pathlib import Path

# Set up argument parser
parser = argparse.ArgumentParser(description="Concatenate multiple CSV files into one and filter by column names.")
parser.add_argument("--CSVfiles", nargs="+", help="List of CSV files to merge")
parser.add_argument("--ColNameFile", help="File containing column names to filter by")
parser.add_argument("--output", default="UntitledMergedCSVFile.csv", help="Output CSV file name")
args = parser.parse_args()

# Read the column-name file ONCE
columns = p.read_csv(Path(args.ColNameFile), header=None)[0].values

def read_and_label(path):
    # Read CSV
    df = p.read_csv(path, encoding="latin1", low_memory=False)

    # Filter to requested columns (strict mode)
    df = df[columns]

    return df

# Read each CSV using the full path
data_frames = [read_and_label(path) for path in args.CSVfiles]

# Stack rows
merged_data_frame = p.concat(data_frames, axis=0)

print(merged_data_frame)

# Save output
merged_data_frame.to_csv(args.output, index=False)


