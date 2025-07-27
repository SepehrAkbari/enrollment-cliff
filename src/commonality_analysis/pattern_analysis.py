import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
import warnings
from preprocess import *
from cluster import *
from pca import *
from cluster_analysis import *
warnings.filterwarnings("ignore")

explanations_df = pd.read_csv('cluster_explanations.csv')

shap.initjs()
explainer = shap.KernelExplainer(kmeans.predict, X)
shap_values = explainer.shap_values(X)

plt.figure(figsize=(10, 8))

plt.rcParams.update({'font.size': 12})
plt.title('Feature Importance to Clustering', pad=10)

shap.summary_plot(
    shap_values,
    X,
    feature_names=feature_names,
    plot_type='bar',
    max_display=20,
    show=False,
    color='tab:blue'
)
ax = plt.gca()

ax.set_xlabel('Mean SHAP Values')

ax.tick_params(axis='y', labelsize=11)
ax.tick_params(axis='x', labelsize=10)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.yticks(ha='right', fontsize=10, va='center', rotation_mode='anchor')
plt.tight_layout()
plt.show()

shap_values_df = pd.DataFrame(shap_values, columns=feature_names)
shap_values_df['name'] = labels['name'].values
shap_values_df.to_csv('shap_values.csv', index=False)