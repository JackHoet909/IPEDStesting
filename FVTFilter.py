import pandas as p
import argparse
from pathlib import Path


parser = argparse.ArgumentParser(description="Synchronize and sort multiple CSV files into one.")
parser.add_argument("--file", help="This is the College Scorecard file to be filtered.")
parser.add_argument("--AJCU", help="This is the AJCU file to align")
parser.add_argument("--Midwest", help="This is the Midwest file to align")
parser.add_argument("--PrivatePublic", help="This is the Private Public file to align")
parser.add_argument("--output", default="UntitledMergedCSVFile1.csv", help="Output CSV file name1") #Sets up a default output name if not explicitly called
args = parser.parse_args() #Parse the arguments when used in the command line


first_df = p.read_csv(Path(args.file), encoding="latin1", index_col=0) #Read the first CSV file

AJCU_df = p.read_csv(Path(args.AJCU), header=None)[0].values #Read the AJCU file and get the values as a list
Midwest_df = p.read_csv(Path(args.Midwest), header=None)[0].values #Read the Midwest file and get the values as a list
PrivatePublic_df = p.read_csv(Path(args.PrivatePublic), header=None)[0].values #Read the Private Public file and get the values as a list

#Filter the first dataframe to only include rows where INSTNM (column header for institution name) is in the list of competitors
reindexed_df = first_df[first_df['CIPCODE'] >= 1000][['INSTNM', 'CONTROL', 'CIPCODE', 'CIPDESC', 'CREDDESC', 'DEBT_ALL_PP_EVAL_MDN', 'EARN_MDN_4YR','EARN_MDN_5YR']]
reindexed_df2 = reindexed_df[reindexed_df['INSTNM'].isin(AJCU_df) | reindexed_df['INSTNM'].isin(Midwest_df) | reindexed_df['INSTNM'].isin(PrivatePublic_df)]

#Create 3 new columns to indicate whether the institution is in each of the three lists (AJCU_FLAG, Midwest_FLAG, and PrivatePublic_FLAG). Give me a Yes or No for each column.
reindexed_df2['AJCU_FLAG'] = reindexed_df2['INSTNM'].isin(AJCU_df).map({True: 'Yes', False: 'No'})
reindexed_df2['Midwest_FLAG'] = reindexed_df2['INSTNM'].isin(Midwest_df).map({True: 'Yes', False: 'No'})
reindexed_df2['PrivatePublic_FLAG'] = reindexed_df2['INSTNM'].isin(PrivatePublic_df).map({True: 'Yes', False: 'No'})


print(reindexed_df2)

reindexed_df2.to_csv(args.output, index=False)

