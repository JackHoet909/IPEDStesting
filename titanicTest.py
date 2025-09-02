import pandas as pd
import argparse
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from pathlib import Path

parser = parser = argparse.ArgumentParser(description="Running machine learning on a CSV file to find clusters.")
parser.add_argument("CSVfile", help="input your csv file") #Allows one or more files to be passed
parser.add_argument("--output", default="UntitledClusteredCSVFile.csv", help="Output CSV file name with its clusters") #Sets up a default output name if not explicitly called
args = parser.parse_args() #Parse the arguments when used in the command line

read_df = pd.read_csv(Path(args.CSVfile), encoding="latin1")
df = pd.get_dummies(read_df)  #perform one-hot encoding on categorical data (transforms strings into a binary set)

columns = df[["Embarked_C", "Embarked_Q", "Embarked_S"]]
scaler = StandardScaler()
columns_Scaled = scaler.fit_transform(columns)

kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
df["Cluster"] = kmeans.fit_predict(columns_Scaled)

print(df)

print(df["Cluster"].value_counts())
df.to_csv(args.output, index=False)



