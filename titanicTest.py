import pandas as pd
import argparse
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from pathlib import Path
import matplotlib.pyplot as plt
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
from sklearn.decomposition import PCA
import seaborn as sns
from sklearn.metrics import pairwise_distances
import numpy as np
from kneed import KneeLocator
from scipy.cluster.hierarchy import linkage, dendrogram





parser = argparse.ArgumentParser(description="Running machine learning on a XLSX file to find clusters.")
parser.add_argument("CSVfile", help="input your csv file") #Allows one or more files to be passed
parser.add_argument("VariableName", nargs="+", help="Input the variable names")
parser.add_argument("--output", default="UntitledClusteredXLSXFile.xlsx", help="Output XLSX file name with its clusters") #Sets up a default output name if not explicitly called
parser.add_argument("--clusters", type=int, default=62, help="Number of clusters to use (default=3)")
parser.add_argument("--hierarchical", action="store_true", help="compute hierarchical clustering")
parser.add_argument("--pairwise", action="store_true", help="compute pair-wise function")
parser.add_argument("--elbow", action="store_true", help="Run elbow method to help determine best cluster count")
args = parser.parse_args() #Parse the arguments when used in the command line

read_df = pd.read_csv(Path(args.CSVfile), encoding="latin1", index_col=0)
#df = pd.get_dummies(read_df)  #perform one-hot encoding on categorical data (transforms strings into a binary set)


read_df = read_df.dropna(subset=args.VariableName) #removes any rows that are missing important info
read_df = read_df.fillna(0) #any missing information gets replaced with a 0


columns = read_df[args.VariableName]
columns_percent = columns.div(columns.sum(axis=1), axis=0) #normalizes total size of each university by converting count to percent
#Drop the column named "Ohio" if it exists
#if "Ohio" in columns_percent.columns:
    #columns_percent = columns_percent.drop(columns="Ohio")
columns_percent = columns_percent.fillna(0)
scaler = StandardScaler()
columns_Scaled = scaler.fit_transform(columns_percent)

# Elbow method
if args.elbow:
    inertia = [] #also known as sum of square distances
    rangeValues = range(1, 100)  #Try k = 1 through 10
    #Fit KMeans for each cluster count and record inertia
    for k in rangeValues:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
        #k represents the amount of clusters
        #random state keeps randomness repeatable. 42 is just a “magic number” people use as a seed
        #n-init will try 10 different starting points and pick the best one
        kmeans.fit(columns_Scaled)
        inertia.append(kmeans.inertia_)
    knee = KneeLocator(rangeValues, inertia, curve="convex", direction="decreasing")

    print("Optimal number of clusters (knee point):", knee.knee)

    sns.set(style="whitegrid")
    sns.lineplot(x=list(rangeValues), y=inertia, marker="o", color="blue")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Inertia (Sum of square distances)")
    plt.title("Elbow Method to Determine Optimal Clusters")
    plt.show()

elif args.pairwise:
    dist_matrix = pairwise_distances(columns_Scaled, metric="euclidean")
    dist_df = pd.DataFrame(dist_matrix, index=read_df.index, columns=read_df.index)
    print(dist_df)
    dist_df.to_excel(args.pairwise, index=True)

elif args.hierarchical:
    #Perform hierarchical clustering (Ward's method)
    linked = linkage(columns_Scaled, method='average')

    #Create figure
    plt.figure(figsize=(10, 7))

    #Plot dendrogram
    dendrogram(
        linked,
        labels=read_df.index.tolist(),      # sample labels
        orientation='top',                  # grow top-down
        distance_sort='descending',         # sort by distance
        show_leaf_counts=True               # show sample count
    )

    plt.style.use('bmh')
    # Title and axis labels
    plt.title('Hierarchical Clustering Dendrogram (Average Linkage)', fontsize=24)
    plt.xlabel('University', fontsize=18)
    plt.ylabel('Distance', fontsize=18)

    # Make university names smaller and angled
    plt.xticks(fontsize=8, rotation=90)  # Smaller font, vertical orientation
    plt.yticks(fontsize=12)

    plt.tight_layout()  # Prevent label cutoff
    plt.show()

else:
    # Run KMeans with chosen cluster count
    kmeans = KMeans(n_clusters=args.clusters, random_state=42, n_init=10)
    read_df["Cluster"] = kmeans.fit_predict(columns_Scaled)

    #Ploting the clusters in 2D using PCA
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(columns_Scaled)
    centers_2d = pca.transform(kmeans.cluster_centers_)


    plt.figure(figsize=(10, 6))
    plt.scatter(data_2d[:, 0], data_2d[:, 1], c=kmeans.labels_, cmap='viridis', edgecolor='k', s=50)
    # Label only "Xavier University"
    for i, name in enumerate(read_df.index):
        if name == "Xavier University":
            plt.scatter(data_2d[i, 0], data_2d[i, 1], color='blue', edgecolor='black', s=100)
        #plt.text(data_2d[i, 0], data_2d[i, 1], name, fontsize=8)
    plt.title('2D Cluster Plot')
    plt.show()

    #Print summary
    val_df = read_df["Cluster"].value_counts()
    print(val_df.to_string())

    
    # Save output
    #read_df.to_excel(args.output, index=True, engine="openpyxl")