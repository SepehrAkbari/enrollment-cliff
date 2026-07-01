'''
Per-cluster analysis
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import math
from preprocess import *
from cluster import *
from pca import *
from cluster_analysis import *
from pattern_analysis import *
warnings.filterwarnings("ignore")


explanations_df = pd.read_csv('cluster_explanations.csv')
shap_values_df = pd.read_csv('shap_values.csv')

def analyze_cluster(cluster_id, data, num_feats=5):
    cluster_indices = np.where(kmeans_labels == cluster_id)[0]
    
    if len(cluster_indices) == 0:
        return "Cluster data not available"
    cluster_shap_values = np.abs(shap_values[cluster_indices])
    
    mean_shap_values = np.mean(cluster_shap_values, axis=0)
    
    feature_importance = {feature: value for feature, value in zip(feature_names, mean_shap_values)}
    
    significant_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    
    return dict(significant_features[:num_feats])

results = {}
for cluster_id in range(optimal_k):
    results[cluster_id] = analyze_cluster(cluster_id, shap_values)

for cluster_id, features in results.items():
    print(f"Cluster {cluster_id} Significant Features:")
    if isinstance(features, dict):
        for feature, score in features.items():
            print(f"  {feature}: {score:.3f}")
    else:
        print(f"    {features}")

def plot_cluster_spider(cluster_id, feature_dict):
    N = len(feature_dict)
    
    max_value = max(feature_dict.values())
    if max_value > 1:
        normalized_values = {k: v / max_value for k, v in feature_dict.items()}
    else:
        normalized_values = feature_dict
    
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], list(normalized_values.keys()), color='tab:red', size=9)
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["", "", "", ""])
    plt.ylim(0, 1)

    values = list(normalized_values.values())
    values += values[:1]

    ax.plot(angles, values, linewidth=2, linestyle='solid', color='tab:blue')
    ax.fill(angles, values, 'tab:blue', alpha=0.1)
    plt.title(f'Cluster {cluster_id} Features', y=1.1)
    plt.tight_layout()
    plt.show()

results = {}
for cluster_id in range(optimal_k):
    results[cluster_id] = analyze_cluster(cluster_id, shap_values)

# cluster_id = 5

# print(f"\nCluster {cluster_id} Significant Features:")
# for feature, score in results[cluster_id].items():
#     print(f"  {feature}: {score:.3f}")

# plot_cluster_spider(cluster_id, results[cluster_id])

for cluster_id in range(optimal_k):
    plot_cluster_spider(cluster_id, results[cluster_id])


def median_across_clusters(feature_name, X, kmeans_labels, feature_names, preprocessor):
    feature_medians = {}
    feature_names_list = feature_names.tolist() if hasattr(feature_names, 'tolist') else feature_names
    scaler = preprocessor.named_transformers_['num']['scaler']
    num_feature_indices = [feature_names_list.index(col) for col in num_cols]
    
    for cluster_id in range(len(set(kmeans_labels))):
        cluster_indices = np.where(kmeans_labels == cluster_id)[0]
        if len(cluster_indices) > 0:
            if feature_name in feature_names_list:
                feature_index = feature_names_list.index(feature_name)
                feature_values_scaled = X[cluster_indices, feature_index]
                if len(feature_values_scaled) > 0:
                    if feature_name in num_cols:
                        feature_num_index = num_feature_indices[num_cols.index(feature_name)]
                        mean_val = scaler.mean_[feature_num_index]
                        scale_val = scaler.scale_[feature_num_index]
                        # z = (x * scale) + mean
                        feature_values_unscaled = (feature_values_scaled * scale_val) + mean_val
                        median_value = np.median(feature_values_unscaled)
                    else:
                        median_value = np.median(feature_values_scaled)
                    feature_medians[cluster_id] = median_value
                else:
                    feature_medians[cluster_id] = None
            else:
                feature_medians[cluster_id] = None
        else:
            feature_medians[cluster_id] = None
    return feature_medians

def shap_across_clusters(feature_name, results):
    feature_shap_values = {}
    for cluster_id in results:
        if isinstance(results[cluster_id], dict) and feature_name in results[cluster_id]:
            cluster_features = results[cluster_id]
            all_values = list(cluster_features.values())
            feature_value = cluster_features[feature_name]
            rank = sum(1 for v in all_values if v > feature_value) + 1
            feature_shap_values[cluster_id] = (rank, feature_value)
        else:
            feature_shap_values[cluster_id] = (None, 0.0)
    return feature_shap_values

feature_to_compare = "endowmentMedian"
shap_values_across_clusters = shap_across_clusters(feature_to_compare, results)

print(f"\nSHAP Values and Ranks for {feature_to_compare} Across All Clusters:")
for cluster_id, (rank, shap_value) in shap_values_across_clusters.items():
    if rank is not None:
        print(f"  Cluster {cluster_id}: Value {shap_value:.3f} (Rank {rank})")
    else:
        print(f"  Cluster {cluster_id}: Value {shap_value:.3f} (Not in top ranks)")

median_values_across_clusters = median_across_clusters(feature_to_compare, X, kmeans_labels, feature_names, preprocessor)
print(f"\nMedian Real Values for {feature_to_compare} Across All Clusters:")
for cluster_id, median_value in median_values_across_clusters.items():
    if median_value is not None:
        print(f"  Cluster {cluster_id}: {median_value:.3f}")
    else:
        print(f"  Cluster {cluster_id}: N/A")