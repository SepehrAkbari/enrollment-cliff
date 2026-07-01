'''
LDA model for topic modeling
'''

import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, LdaModel
import pickle
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv("processed_article_content.csv")
dictionary = Dictionary.load("article_dictionary.gensim")
with open("corpus_tfidf.pkl", "rb") as f:
    corpus_tfidf = pickle.load(f)

num_topics = 4

lda_model = LdaModel(corpus=corpus_tfidf, 
                     id2word=dictionary, 
                     num_topics=num_topics, 
                     passes=15, 
                     random_state=42)
topics = lda_model.print_topics(num_words=20)
# for topic in topics:
#     print(topic)

topics_df = pd.DataFrame(topics, columns=['Topic ID', 'Words'])
topics_df['Words'] = topics_df['Words'].apply(
    lambda x: dict([
        (word_part.split('*')[1].strip('"'), float(word_part.split('*')[0]))
        for word_part in x.split(' +')
    ])
)

# for index, row in topics_df.iterrows():
#     print(f"Topic {row['Topic ID']}:")
#     for word, freq in row['Words'].items():
#         print(f"  {word}: {freq}")
#     print()