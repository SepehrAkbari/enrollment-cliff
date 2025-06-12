import pandas as pd
import numpy as np

df = pd.read_csv("endowments.csv")

years = [2024, 2023, 2022, 2021, 2020, 2019, 2018]
endowment_cols = [f'EndowmentMedian{year}' for year in years]

def quadratic_imputation(row, endowment_cols, years):
    values = [row[col] if pd.notnull(row[col]) and row[col] != 0 else np.nan for col in endowment_cols]
    valid_indices = [i for i, val in enumerate(values) if not np.isnan(val)]
    valid_years = [years[i] for i in valid_indices]
    valid_values = [values[i] for i in valid_indices]
    
    if len(valid_values) < 3:
        return row
    
    try:
        coeffs = np.polyfit(valid_years, valid_values, deg=2)
        poly = np.poly1d(coeffs)
        
        for i, col in enumerate(endowment_cols):
            if pd.isnull(values[i]) or values[i] == 0:
                imputed_value = poly(years[i])
                row[col] = max(0, imputed_value)
    except np.linalg.LinAlgError:
        return row
    
    return row

mask = (df['noData'] == False) & (df['hasMissing'] == True)
df_imputed = df.copy()

df_imputed.loc[mask] = df_imputed.loc[mask].apply(
    lambda row: quadratic_imputation(row, endowment_cols, years), axis=1
)

df_imputed.to_csv('endowments_imputed.csv', index=False)