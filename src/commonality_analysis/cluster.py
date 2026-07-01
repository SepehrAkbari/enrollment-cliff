'''
K-Means clustering
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.manifold import TSNE
import warnings
from preprocess import *
warnings.filterwarnings("ignore")


inertia = []
k_range = range(2, 40)
for k in k_range:
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=rs)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(12, 8))
plt.plot(k_range, inertia, marker='x', color='tab:blue')
plt.xlabel('Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.grid()
plt.show()

silhouettes = []
for k in range(2, 40):
    kmeans = KMeans(n_clusters=k, random_state=rs, n_init=10)
    kmeans.fit(X)
    silhouettes.append(metrics.silhouette_score(X, kmeans.labels_))

plt.figure(figsize=(12, 8))
plt.plot(k_range, silhouettes, marker='x', color='tab:blue')
plt.xlabel('Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score of Clusters [shape: (65, 66)]')
plt.grid()
plt.show()

print("Top 5 optimal-k candidates:")
for idx in np.argsort(silhouettes)[-5:][::-1]:
    print(f"k = {k_range[idx]} ({silhouettes[idx]:.4f})")

print("chosen k = 21")
optimal_k = 21

kmeans = KMeans(n_clusters=optimal_k, random_state=rs)
kmeans_labels = kmeans.fit_predict(X)

plt.figure(figsize=(12, 8))
labels['kmeans_cluster'] = kmeans_labels
labels['kmeans_cluster'].value_counts().sort_index().plot(kind='bar', color='tab:gray', edgecolor='black', width=0.75)
plt.xlabel('Cluster')
plt.ylabel('Count')
plt.title(f'K-Means Clusters (k={optimal_k})')
plt.show()

tsne = TSNE(n_components=2, perplexity=30, learning_rate=200, random_state=42)
X_tsne = tsne.fit_transform(X)

labels['tsne_x'] = X_tsne[:, 0]
labels['tsne_y'] = X_tsne[:, 1]

plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(x=X_tsne[:, 0], y=X_tsne[:, 1], hue=kmeans_labels, palette=tab_colors, s=100)
# for i, name in enumerate(labels['name']):
#     plt.text(X_tsne[i, 0], X_tsne[i, 1], name, fontsize=8)
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.title('t-SNE with Clusters')
plt.legend(title='Cluster', loc='upper right', bbox_to_anchor=(1.1, 1))

plt.show()