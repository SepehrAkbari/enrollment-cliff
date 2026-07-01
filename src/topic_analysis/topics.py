'''
Topic visualization
'''

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings
from model import topics_df
warnings.filterwarnings("ignore")


def visualize_dictionary(word_frequencies_dict):
    wordcloud = WordCloud(width=800, 
                          height=400, 
                          background_color='white', 
                          colormap='managua').generate_from_frequencies(word_frequencies_dict)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.grid(False)
    plt.tight_layout()
    plt.show()

    sorted_words = sorted(word_frequencies_dict.items(), key=lambda item: item[1], reverse=True)
    words = [item[0] for item in sorted_words]
    frequencies = [item[1] for item in sorted_words]

    plt.figure(figsize=(10, 5))
    plt.bar(words, frequencies, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

for i in range(len(topics_df)):
    topic_id_to_visualize = topics_df.iloc[i]['Topic ID']
    word_dictionary_for_topic = topics_df.iloc[i]['Words']

    visualize_dictionary(word_dictionary_for_topic)