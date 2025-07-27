import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns
from sklearn.decomposition import PCA
import warnings
from preprocess import *
from cluster import *
warnings.filterwarnings("ignore")

pca = PCA(random_state=rs)
X_pca = pca.fit_transform(X)

eigenvalues = pca.explained_variance_
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance_ratio)

n_components_95 = np.argmax(cumulative_variance >= 0.95) + 1

for i in range(5):
    labels[f'pca_component_{i+1}'] = X_pca[:, i]

plt.figure(figsize=(12, 8))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=kmeans_labels, palette=tab_colors, s=100)
# for i, name in enumerate(labels['name']):
#     plt.text(X_pca[i, 0], X_pca[i, 1], name, fontsize=8)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of K-Means Clusters (k=21)')
plt.legend(title='Clusters', loc='upper right', bbox_to_anchor=(1.1, 1))
plt.tight_layout()
plt.show()

print(f"\nEigenvalues: \n{eigenvalues[:10]}")
print(f"\nExplained Variance Ratio: \n{explained_variance_ratio[:10]}")
print(f"\nNumber of PCs for 95% variance: {n_components_95}")
print(f"\nVariance explained by top 5 PCs: {cumulative_variance[4]*100:.2f}%")

plt.figure(figsize=(12, 8))
component_loadings = pca.components_.T

scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c='tab:green', alpha=0.5, s=100, edgecolor='tab:olive')

scaling = np.max(np.abs(X_pca[:, :2])) / np.max(np.abs(component_loadings[:, :2])) * 0.7

feature_importance = np.sum(np.abs(component_loadings[:, :2]), axis=1)
top_indices = np.argsort(-feature_importance)[:10]

for i in top_indices:
    name = feature_names[i]
    if len(name) > 25:
        name = name[:22] + "..."
    
    plt.arrow(0, 0, 
              component_loadings[i, 0] * scaling, 
              component_loadings[i, 1] * scaling, 
              color='tab:red', alpha=0.6, 
              head_width=0.3, head_length=0.3)
    
    # text_x = component_loadings[i, 0] * scaling * 1.15
    # text_y = component_loadings[i, 1] * scaling * 1.15
    
    # plt.text(text_x, text_y, name, 
    #          color='darkred', fontsize=9, fontweight='bold',
    #          ha='center', va='center')

plt.xlabel(f'Principal Component 1 ({explained_variance_ratio[0]*100:.1f}%)')
plt.ylabel(f'Principal Component 2 ({explained_variance_ratio[1]*100:.1f}%)')
plt.title('Top Features (10) Contribution to Principal Components')

plt.axhline(y=0, color='gray', linestyle='--', alpha=0.4)
plt.axvline(x=0, color='gray', linestyle='--', alpha=0.4)
plt.grid(alpha=0.2)

# Add some annotations about variance
# plt.annotate(f'Total variance explained: {(cumulative_variance[1])*100:.1f}%', 
#              xy=(0.02, 0.98), xycoords='axes fraction',
#              fontsize=12, fontweight='bold',
#              bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.tight_layout()
plt.show()

print("Top 10 features contributing to the first two principal components:")
for i in top_indices:
    name = feature_names[i]
    if len(name) > 25:
        name = name[:22]
    print(f"{i+1}. {name} ({feature_importance[i]:.4f})")

pc2_loadings = pca.components_[1, :]
pc1_loadings = pca.components_[0, :]

feature_importance_pc2 = np.abs(pc2_loadings)
feature_importance_pc1 = np.abs(pc1_loadings)

top_indices_pc2 = np.argsort(-feature_importance_pc2)[:10]
top_indices_pc1 = np.argsort(-feature_importance_pc1)[:10]

plt.figure(figsize=(12, 8))
feature_names_short = [name[:25] + '...' if len(name) > 25 else name for name in feature_names[top_indices_pc2]]
colors = ['tab:blue' if pc2_loadings[i] > 0 else 'tab:red' for i in top_indices_pc2]

bars = plt.barh(range(len(top_indices_pc2)), feature_importance_pc2[top_indices_pc2], color=colors)
plt.yticks(range(len(top_indices_pc2)), feature_names_short)
plt.xlabel('Absolute Contribution to PC2')
plt.title('Top 10 Features Contributing to Principal Component 2')

legend_elements = [
    Patch(facecolor='tab:blue', label='Positive Contribution'),
    Patch(facecolor='tab:red', label='Negative Contribution')
]
plt.legend(handles=legend_elements, loc='lower right')

for i, bar in enumerate(bars):
    original_value = pc2_loadings[top_indices_pc2[i]]
    plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
             f'{original_value:.3f}', va='center')

plt.tight_layout()
plt.show()

print("\nTop 10 features contributing to Principal Component 2:")
for i, idx in enumerate(top_indices_pc2):
    direction = "positive" if pc2_loadings[idx] > 0 else "negative"
    print(f"{i+1}. {feature_names[idx]} ({direction}): {pc2_loadings[idx]:.4f}")

plt.figure(figsize=(12, 8))
feature_names_short = [name[:25] + '...' if len(name) > 25 else name for name in feature_names[top_indices_pc1]]
colors = ['tab:blue' if pc1_loadings[i] > 0 else 'tab:red' for i in top_indices_pc1]

bars = plt.barh(range(len(top_indices_pc1)), feature_importance_pc1[top_indices_pc1], color=colors)
plt.yticks(range(len(top_indices_pc1)), feature_names_short)
plt.xlabel('Absolute Contribution to PC1')
plt.title('Top 10 Features Contributing to Principal Component 1')

legend_elements = [
    Patch(facecolor='tab:blue', label='Positive Contribution'),
    Patch(facecolor='tab:red', label='Negative Contribution')
]
plt.legend(handles=legend_elements, loc='lower right')

for i, bar in enumerate(bars):
    original_value = pc1_loadings[top_indices_pc1[i]]
    plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
             f'{original_value:.3f}', va='center')

plt.tight_layout()
plt.show()

print("\nTop 10 features contributing to Principal Component 1:")
for i, idx in enumerate(top_indices_pc1):
    direction = "positive" if pc1_loadings[idx] > 0 else "negative"
    print(f"{i+1}. {feature_names[idx]} ({direction}): {pc1_loadings[idx]:.4f}")

plt.figure(figsize=(12, 8))
plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, marker='o', color='tab:blue')
plt.xlabel('Principal Component')
plt.ylabel('Eigenvalue')
plt.title('Eigenvalues of Principal Components')
plt.grid()
plt.axhline(y=0, color='k', linestyle='--', alpha=0.5)
plt.axvline(x=5.5, color='k', linestyle='--', alpha=0.5)

vline_x_position1 = 5.8
vline_y_position1 = max(eigenvalues) * 0.9

plt.text(vline_x_position1, vline_y_position1, '72.2% of the variance',
         rotation=90,
         verticalalignment='top',
         fontsize=10,
         color='k',
         alpha=0.9)


plt.axvline(x=17.5, color='k', linestyle='--', alpha=0.5)

vline_x_position2 = 17.8
vline_y_position2 = max(eigenvalues) * 0.9

plt.text(vline_x_position2, vline_y_position2, '95% of the variance',
         rotation=90,
         verticalalignment='top',
         fontsize=10,
         color='k',
         alpha=0.9)


x_offset = 1.2
y_offset = 0.2

for i, val in enumerate(eigenvalues[:3]):
    plt.text(i + 1 + x_offset, val + y_offset, f'{val:.2f}',
             fontsize=10,
             fontweight='bold',
             ha='center',
             va='center',
             color='tab:blue',
             alpha=0.8)
x_offset1 = 0.5
y_offset1 = -0.4
for i, val in enumerate(eigenvalues[3:5]):
    plt.text(i + 1 + x_offset1, val + y_offset1, f'{val:.2f}',
             fontsize=10,
             fontweight='bold',
             ha='left',
             va='bottom',
             color='tab:blue',
             alpha=0.8)
plt.legend()
plt.tight_layout()
plt.show()