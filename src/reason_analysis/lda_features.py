import pandas as pd
import warnings
from src.commonality_analysis.preprocess import *
from src.commonality_analysis.cluster import *
from src.commonality_analysis.pca import *
from lda import *
warnings.filterwarnings("ignore")

feature_names = X_processed.columns.tolist()

coef_df = pd.DataFrame(lda_reason.coef_, columns=feature_names)

component_labels = [f'Component {i+1}' for i in range(lda_reason.coef_.shape[0])]
coef_df.index = component_labels

for i, component_name in enumerate(component_labels):
    print(f"\n{component_name} is primarily influenced by:")
    sorted_features = coef_df.iloc[i].abs().sort_values(ascending=False)
    top_n = 10
    for feature, strength in sorted_features.head(top_n).items():
        original_coefficient = coef_df.loc[component_name, feature]
        print(f"  - {feature}: {original_coefficient:.4f} (Magnitude: {strength:.4f})")

labels.to_csv('lda_results.csv', index=False)