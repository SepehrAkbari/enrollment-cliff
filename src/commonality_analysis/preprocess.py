'''
Data preprocessing
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps as cm
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings("ignore")


rs = 42
np.random.seed(rs)
df = pd.read_excel("data.xlsx")
for x in ['religionAffiliation', 
          'specialDemographic', 
          'mergingInstitutionPopulation', 
          'mergingInstitutionType', 
          'mergingInstitutionLocationType', 
          'mergingInstitutionReligiousAffiliation',]:
    df[x] = df[x].fillna('None')
df['endowmentMedian'] = df['endowmentMedian'].fillna(-1)
df.drop(columns=['mergingInstitutionPopulation'], inplace=True)

colors_tab20 = cm['tab20'].resampled(20).colors
colors_tab20b = cm['tab20b'].resampled(20).colors
tab_colors = list(colors_tab20) + list(colors_tab20b)

df.loc[df['name'].isin(['Independence University', 'Alliance University (Formerly Nyack College)']), 'reasonFinancial'] = True

reason_cols = ['reasonFinancial', 'reasonEnrollment', 'reasonPandemic', 'reasonMutualBenefit']
def create_reason_closure(row):
    reasons = [str(i) for i, reason in enumerate(reason_cols) if row[reason]]
    return ''.join(sorted(reasons)) if reasons else 'None'

df['reasonClosure'] = df.apply(create_reason_closure, axis=1)

labels = df[['name', 'reasonClosure']].copy()
label_cols = ['name', 'reasonClosure', 'state', 'stateAbbreviation', 'region']
lessImpact_cols = ['yearClosed', 'yearEstablished', 'typeProfit', 'religionAffiliation',
                  'specialDemographic', 'mergingInstitutionType',
                  'mergingInstitutionLocationType', 'mergingInstitutionReligiousAffiliation',
                  'stateBirths', 'stateFemalePopulation', 'regionFemalePopulation', 'regionBirths']
X_df = df.drop(columns=label_cols + lessImpact_cols + reason_cols)

cat_cols = X_df.select_dtypes(include=['object', 'bool']).columns.tolist()
num_cols = X_df.select_dtypes(include=['float64', 'int64']).columns.tolist()

num_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

cat_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop='first'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transformer, num_cols),
        ('cat', cat_transformer, cat_cols)
    ])

X = preprocessor.fit_transform(X_df)

cat_feature_names = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(cat_cols)
feature_names = np.concatenate([num_cols, cat_feature_names])
X_processed = pd.DataFrame(X, columns=feature_names)