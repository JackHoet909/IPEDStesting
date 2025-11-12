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
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples






parser = argparse.ArgumentParser(description="Running machine learning on a XLSX file to find clusters.")
parser.add_argument("CSVfile", help="input your csv file") #Allows one or more files to be passed
parser.add_argument("VariableName", nargs="+", help="Input the variable names")
parser.add_argument("--output", help="Output XLSX file name with its clusters") #Sets up a default output name if not explicitly called
parser.add_argument("--clusters", type=int, default=62, help="Number of clusters to use (default=3)")
parser.add_argument("--UniNameFile", help="Input the file of the list of univerities to highlight on dendrogram")
parser.add_argument("--hierarchical", action="store_true", help="compute hierarchical clustering")
parser.add_argument("--pairwise", action="store_true", help="compute pair-wise function")
parser.add_argument("--rank", type=str, nargs = "+", help="rank states for a given university (make sure to quote the name if there's spaces)")
parser.add_argument("--silhouette", action="store_true", help="compute silhouette scores")
parser.add_argument("--elbow", action="store_true", help="Run elbow method to help determine best cluster count")
parser.add_argument("--c", type=int, default=62, help="Count of states in the ranking")
parser.add_argument("--linkage", type=str, default="ward", help="Linkage method for hierarchical clustering (ward, single, complete, average)")
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
scaler = StandardScaler()
scaler.fit(columns_percent)
columns_Scaled = scaler.transform(columns_percent)

#Rebuild a DataFrame with university names and state columns
scaled_df = pd.DataFrame(columns_Scaled, index=columns.index, columns=columns.columns)


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

elif args.rank:
    def get_ranked_states_scaled(university_name, top_n):
        if university_name not in scaled_df.index:
            print(f"University '{university_name}' not found in the dataset.")
            return None
        # Get scaled state scores for the university
        state_scores = scaled_df.loc[university_name]
        ranked = state_scores.sort_values(ascending=False).head(top_n)
        # Return a clean two-column DataFrame
        return pd.DataFrame({
            f"{university_name} State": ranked.index,
            f"{university_name} Score": ranked.values
        })

    # Collect rankings for each university
    ranked_frames = []
    for name in args.rank:
        df = get_ranked_states_scaled(name, args.c)
        if df is not None:
            ranked_frames.append(df.reset_index(drop=True))

    # Concatenate side-by-side
    combined_df = pd.concat(ranked_frames, axis=1)
    if args.output:
        # Save to Excel
        combined_df.to_excel(args.output, index=False, engine="openpyxl")
    print(combined_df)

    

elif args.pairwise:
    dist_matrix = pairwise_distances(columns_Scaled, metric="euclidean")
    dist_df = pd.DataFrame(dist_matrix, index=read_df.index, columns=read_df.index)
    print(dist_df)
    dist_df.to_excel(args.output, index=True, engine="openpyxl")

elif args.hierarchical:
    #Perform hierarchical clustering (Ward's method)
    linked = linkage(columns_Scaled, method=args.linkage)

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
    
    ax = plt.gca() #Get current axes
    x_tick_labels = ax.get_xticklabels() #Get the x-axis tick labels

    highlight_universities = pd.read_csv(Path(args.UniNameFile), header=None)[0].values #Read the list of universities to highlight

    for label_obj in x_tick_labels: #For each label on the x-axis 
        if label_obj.get_text() in highlight_universities: #If the label is in the list of universities to highlight
            label_obj.set_color('red')
            label_obj.set_fontweight('bold') #Make it bolded red

    plt.style.use('bmh')
    # Title and axis labels
    plt.title('Hierarchical Clustering Dendrogram (' + args.linkage + " linkage)", fontsize=24)
    plt.xlabel('University', fontsize=18)
    plt.ylabel('Distance', fontsize=18)

    # Make university names smaller and angled
    plt.xticks(fontsize=8, rotation=90)  # Smaller font, vertical orientation
    plt.yticks(fontsize=12)

    plt.tight_layout()  # Prevent label cutoff
    plt.show()
    
elif args.silhouette:
    scores = []
    rangeValues = range(2, 100)  #Try k = 2 through 100
    for k in rangeValues: #for each cluster count
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10) #Fit KMeans
        labels = kmeans.fit_predict(columns_Scaled) #predict clusters for each point
        #Calculate silhouette score for Xavier University
        sample_score = silhouette_samples(columns_Scaled, kmeans.labels_)
        xavier_index = read_df.index.get_loc("Xavier University")
        xavier_score = sample_score[xavier_index]
        scores.append(xavier_score)
    
    plt.plot(rangeValues, scores, marker='o')
    plt.title('Xavier Silhouette Scores (Percent of Each State)')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Silhouette Score')
    plt.grid(True)
    plt.show()

else:
    # Run KMeans with chosen cluster count
    kmeans = KMeans(n_clusters=args.clusters, random_state=42, n_init=10)
    read_df["Cluster"] = kmeans.fit_predict(columns_Scaled)

    score = silhouette_score(columns_Scaled, kmeans.labels_)
    print(f"Silhouette Score: {score:.3f}")

    sample_score = silhouette_samples(columns_Scaled, kmeans.labels_)
    xavier_index = read_df.index.get_loc("Xavier University")
    xavier_score = sample_score[xavier_index]
    print(f"Xavier University's Silhouette Score: {xavier_score:.3f}") #Print silhouette score for Xavier University if it exists (3 decimal places)

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
    read_df.to_excel(args.output, index=True, engine="openpyxl")