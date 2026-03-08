import pandas as pd
from pathlib import Path
import argparse

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--InstitutionalFile", help="Path to the input CSV file")
parser.add_argument("--EnrollmentFile", help="Path to the second input CSV file")
parser.add_argument("--output", required=True)
args = parser.parse_args()

#Read the CSV
ins_df = pd.read_csv(Path(args.InstitutionalFile), encoding="latin1", low_memory=False)
enroll_df = pd.read_csv(Path(args.EnrollmentFile), encoding="latin1", low_memory=False)

#remove rows where EFCState has value 99 and 58 (enrollment file)
enroll_filtered = enroll_df[~enroll_df["EFCSTATE"].isin([99, 58])]

#remove rows where ICLEVEL is not 1 and CONTROL is not 1 or 2 (institutional file)
inst_filtered = ins_df[(ins_df["ICLEVEL"] == 1) & (ins_df["CONTROL"].isin([1, 2]))]

#merge the two filtered dataframes on UNITID
filtered_df = pd.merge(enroll_filtered, inst_filtered, on="UNITID", how="inner")
filtered_df = filtered_df[["UNITID", "EFCSTATE", "EFRES01"]] 

print(filtered_df)
filtered_df.to_csv(args.output, index=False)
