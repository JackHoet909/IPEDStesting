import pandas as pd
import argparse
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from pathlib import Path
import matplotlib.pyplot as plt
from openpyxl.workbook import Workbook
from sklearn.decomposition import PCA
import seaborn as sns
import numpy as np


parser = argparse.ArgumentParser(description="Running machine learning on a CSV file to find clusters.")
parser.add_argument("CSVfile", help="input your csv file") #Allows one or more files to be passed
parser.add_argument("VariableName", nargs="+", help="Input the variable names")
parser.add_argument("--output", default="UntitledClusteredCSVFile.csv", help="Output CSV file name with its clusters") #Sets up a default output name if not explicitly called
parser.add_argument("--clusters", type=int, default=5, help="Number of clusters to use (default=3)")
parser.add_argument("--elbow", action="store_true", help="Run elbow method to help determine best cluster count")
args = parser.parse_args() #Parse the arguments when used in the command line

read_df = pd.read_csv(Path(args.CSVfile), encoding="latin1")
#df = pd.get_dummies(read_df)  #perform one-hot encoding on categorical data (transforms strings into a binary set)

read_df = read_df.dropna(subset=args.VariableName) #removes any rows that are missing important info
read_df = read_df.fillna(0) #any missing information gets replaced with a 0

columns = read_df[args.VariableName]
columns_percent = columns.div(columns.sum(axis=1), axis=0) #normalizes total size of each univeristy by converting count to percent
scaler = StandardScaler()
columns_Scaled = scaler.fit_transform(columns_percent)

# Elbow method
if args.elbow:
    inertia = [] #also known as sum of square distances
    rangeValues = range(1, 11)  #Try k = 1 through 10
    #Fit KMeans for each cluster count and record inertia
    for k in rangeValues:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
        #k represents the amount of clusters
        #random state keeps randomness repeatable. 42 is just a “magic number” people use as a seed
        #n-init will try 10 different starting points and pick the best one
        kmeans.fit(columns_Scaled)
        inertia.append(kmeans.inertia_)

    sns.set(style="whitegrid")
    sns.lineplot(x=list(rangeValues), y=inertia, marker="o", color="blue")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Inertia (Sum of square distances)")
    plt.title("Elbow Method to Determine Optimal Clusters")
    plt.show()
else:
    # Run KMeans with chosen cluster count
    kmeans = KMeans(n_clusters=args.clusters, random_state=42, n_init=10)
    read_df["Cluster"] = kmeans.fit_predict(columns_Scaled)


    #Ploting the clusters in 2D using PCA
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(columns_Scaled)
    plt.figure(figsize=(8,6)) #making the picture 8 inches wide and 6 inches long

    #Draw your data points as dots on the canvas. Each dot's position comes from the 2D PCA data
    #The color of each dot comes from its cluster number
    plt.scatter(data_2d[:, 0], data_2d[:, 1], c=read_df["Cluster"], cmap='tab10', s=30)
    # Loop through each point and add a label
    for i in range(len(data_2d)):
        x = data_2d[i, 0]  # X position from PCA
        y = data_2d[i, 1]  # Y position from PCA
        name = read_df["University Name"].iloc[i]  # Get the university name
        plt.text(x, y, name, fontsize=8, alpha=0.6)  # Add the label near the dot
    
    plt.legend()
    plt.title("2D Cluster Plot") 
    plt.grid(True)
    plt.show()


    #cluster-to-color mapping for EXCEL FILE (output)
    cluster_colors = {0: 'lightblue', 1: 'lightgreen', 2: 'lightcoral', 3: 'khaki', 4: 'plum', 5: 'lightyellow'}
    # Function to apply row-wise background color
    def highlight_cluster(row):
        color = cluster_colors.get(row['Cluster'], 'white')
        return ['background-color: {}'.format(color)] * len(row)
    
    # Apply styling
    styled_df = read_df.style.apply(highlight_cluster, axis=1)
    #Print summary
    print(read_df["Cluster"].value_counts())
    # Save output
    styled_df.to_excel(args.output, index=False)