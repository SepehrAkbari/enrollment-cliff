import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import warnings
from src.commonality_analysis.preprocess import *
from src.commonality_analysis.cluster import *
from src.commonality_analysis.pca import *
warnings.filterwarnings("ignore")

reason_closure_map = {
    '0': 'Financial',
    '1': 'Enrollment',
    '2': 'Pandemic',
    '3': 'Mutual Benefit',
    '12': 'Enrollment and Pandemic',
    '012': 'Financial and Enrollment and Pandemic',
    '02': 'Financial and Pandemic',
    '01': 'Financial and Enrollment'
}
y_reason = labels['reasonClosure']
if len(np.unique(y_reason)) > 1:
    n_components = min(len(np.unique(y_reason)) - 1, X.shape[1])
    lda_reason = LinearDiscriminantAnalysis(n_components=n_components)
    X_lda_reason = lda_reason.fit_transform(X, y_reason)
    
    for i in range(X_lda_reason.shape[1]):
        labels[f'lda_reason_component_{i+1}'] = X_lda_reason[:, i]
    
    if X_lda_reason.shape[1] >= 2:
        y_reason_mapped = y_reason.map(reason_closure_map)
        plt.figure(figsize=(12, 8))
        sns.scatterplot(x=X_lda_reason[:, 0], y=X_lda_reason[:, 1], hue=y_reason_mapped, palette='tab10', s=100, legend='full')
        # for i, name in enumerate(labels['name']):
        #     plt.text(X_lda_reason[i, 0], X_lda_reason[i, 1], name, fontsize=8)
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.title('LDA of Closure Reasons')
        plt.legend(title='Closure Reason', loc='lower right')
        plt.show()
    
    print(f"\nExplained Variance Ratio: \n{lda_reason.explained_variance_ratio_}\n")
    for reason in np.unique(y_reason):
        if reason == '0':
            label = 'Financial'
        elif reason == '1':
            label = 'Enrollment'
        elif reason == '2':
            label = 'Pandemic'
        elif reason == '3':
            label = 'Mutual Benefit'
        elif reason == '12':
            label = 'Enrollment and Pandemic'
        elif reason == '012':
            label = 'Financial and Enrollment and Pandemic'
        elif reason == '02':
            label = 'Financial and Pandemic'
        elif reason == '01':
            label = 'Financial and Enrollment'
        print(f"{label}:\n{labels[labels['reasonClosure'] == reason]['name'].values}\n")