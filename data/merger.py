import pandas as pd

colleges_df = pd.read_csv('colleges.csv')
states_df = pd.read_csv('states.csv')
media_df = pd.read_csv('media_articles.csv')
colleges_df_copy = colleges_df.copy()
states_df_copy = states_df.copy()
media_df_copy = media_df.copy()

states_to_join = states_df_copy.drop(columns=['state'])
merged_df = pd.merge(colleges_df_copy, states_to_join, on='state_abbr', how='left')

columns_to_drop = ['uid', 'key', 'state', 'year_closed']
media_to_join = media_df_copy.drop(columns=columns_to_drop, errors='ignore')

final_merged_df = pd.merge(merged_df, media_to_join, on='name', how='left')

final_merged_df.to_csv('merged.csv', index=False)
final_merged_df.to_excel('merged.xlsx', index=False)