import pandas as pd

colleges_xsl = pd.read_excel('colleges.xlsx')
states_xsl = pd.read_excel('states.xlsx')
media_xsl = pd.read_excel('media_articles.xlsx')

colleges_xsl.to_csv('colleges.csv', index=False)
states_xsl.to_csv('states.csv', index=False)
media_xsl.to_csv('media_articles.csv', index=False)