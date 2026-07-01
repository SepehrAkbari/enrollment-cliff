'''
Analysis on clusters
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from preprocess import *
from cluster import *
from pca import *
warnings.filterwarnings("ignore")


print(f"Cluster Sizes: \n\n{labels['kmeans_cluster'].value_counts(normalize=True)}")

print("\nTop Features per K-Means Cluster (Mean):")
for cluster in range(optimal_k):
    cluster_data = X_processed[labels['kmeans_cluster'] == cluster]
    print(f"\nCluster {cluster} Top 5 Features:")
    print(cluster_data.mean().sort_values(ascending=True).head(5))

print("\nTop Features per Cluster (by Variance):")
for cluster in range(optimal_k):
    cluster_data = X_processed[labels['kmeans_cluster'] == cluster]
    print(f"\nCluster {cluster} Top 5 Features:")
    print(cluster_data.var().sort_values(ascending=False).head(10))

centroids = kmeans.cluster_centers_
college_explanations = []
for i in range(X.shape[0]):
    cluster = kmeans_labels[i]
    distances = np.abs(X[i] - centroids[cluster])
    sum_distances = distances.sum()
    if sum_distances > 0:
        contributions = distances / sum_distances
    else:
        contributions = np.zeros_like(distances)
    
    top_features_idx = np.argsort(contributions)[::-1][:5]
    
    feature_names_list = feature_names.tolist() if hasattr(feature_names, 'tolist') else list(feature_names)
    
    top_features = [feature_names_list[idx] for idx in top_features_idx]
    top_contributions = contributions[top_features_idx]
    
    college_explanations.append({
        'name': labels['name'].iloc[i],
        'cluster': cluster,
        'top_feature_1': top_features[0],
        'impact_1': top_contributions[0],
        'top_feature_2': top_features[1],
        'impact_2': top_contributions[1],
        'top_feature_3': top_features[2],
        'impact_3': top_contributions[2],
        'top_feature_4': top_features[3],
        'impact_4': top_contributions[3],
        'top_feature_5': top_features[4],
        'impact_5': top_contributions[4]
    })

explanations_df = pd.DataFrame(college_explanations)
explanations_df.to_csv('cluster_explanations.csv', index=False)

for cluster in range(optimal_k):
    cluster_explanations = explanations_df[explanations_df['cluster'] == cluster]
    feature_counts = {}
    for i in range(1, 6):
        col = f'top_feature_{i}'
        for feature in cluster_explanations[col]:
            feature_counts[feature] = feature_counts.get(feature, 0) + 1
    feature_counts_df = pd.DataFrame.from_dict(feature_counts, orient='index', columns=['Count'])
    feature_counts_df = feature_counts_df.sort_values('Count', ascending=False).head(5)
    print(f"\nCluster {cluster} Top Features by Frequency in Explanations:")
    print(feature_counts_df)

feature_freq_df = pd.DataFrame()

for cluster in range(optimal_k):
    cluster_explanations = explanations_df[explanations_df['cluster'] == cluster]
    feature_counts = {}
    for i in range(1, 6):
        col = f'top_feature_{i}'
        for feature in cluster_explanations[col]:
            feature_counts[feature] = feature_counts.get(feature, 0) + 1
    
    feature_counts_df = pd.DataFrame.from_dict(feature_counts, orient='index', columns=[f'Cluster {cluster}'])
    feature_freq_df = pd.concat([feature_freq_df, feature_counts_df], axis=1)

feature_freq_df = feature_freq_df.fillna(0)

top_features = feature_freq_df.sum(axis=1).sort_values(ascending=False).head(15).index

plt.figure(figsize=(18, 12))
sns.heatmap(feature_freq_df.loc[top_features].T, cmap='Oranges', annot=True, fmt='.0f', linewidths=0.5, cbar_kws={'label': 'Frequency'}, cbar=False)
plt.title('Frequency of Top Features Across Clusters', fontsize=14)
plt.ylabel('')
plt.xlabel('')
plt.xticks(rotation=25, ha='right')
plt.tight_layout()
plt.show()