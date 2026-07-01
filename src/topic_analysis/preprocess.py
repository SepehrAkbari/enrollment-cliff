'''
Preprocessing article content
'''

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, LdaModel
import ssl
import pickle
import warnings
from dataset import df
warnings.filterwarnings("ignore")


df.drop(columns=['hed', 'article'], inplace=True)

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

lemmatizer = WordNetLemmatizer()
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

college_names = df['name']
college_df = college_names.str.replace(r'\b(College|University|School|Campus)\b', '', regex=True).str.strip()
location_names = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
                "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
                "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
                "Montana", "Nebraska", "Nevada", "New", "Hampshire", "Jersey", "Mexico", "York",
                "Carolina", "North", "Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
                "Rhode Island", "South Carolina", "South", "Dakota", "Tennessee", "Texas",
                "Utah", "Vermont", "Virginia", "Washington", "West", 'ann', 'arbor', 'boston', 'brooklyn', 'chicago', 'dallas',
                'denver', 'detroit', 'houston', 'las', 'vegas', 'los', 'angeles', 'miami', 'minneapolis',
                'new', 'orleans', 'new', 'york', 'philadelphia', 'phoenix', 'portland', 'san', 'antonio',
                'san', 'diego', 'san', 'francisco', 'seattle', 'washington', 'dc', 'atlanta',
                "Wisconsin", "Wyoming", "District", "Columbia", "Puerto", "Rico", "Indianapolis", "Chicago", "Los", "Angeles", "City", "Staten", "Island",
                'waukesha', 'milwaukee', 'bloomfield', 'uwm', 'redlands', 'stritch', 'uwplatteville', 'uwmadison',
                'uwoshkosh', 'uwgreenbay', 'uwlacrosse', 'uwstevenspoint', 'uwsuperior', 'uwwhitewater', 'southern', 'northern', 'central', 'eastern', 'western']
location_df = pd.DataFrame(location_names, columns=['name'])
time_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 
              'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
              'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
              'AM', 'PM', 'morning', 'afternoon', 'evening', 'night',
              'today', 'tomorrow', 'yesterday', 'now', 'soon', 'later', 'week', 'month', 'year',
              'weekend', 'holiday', 'vacation', 'break', 'semester', 'quarter', 'session', 'class', 'course',
              'schedule', 'timetable', 'appointment', 'meeting', 'event', 'deadline', 'due date']
time_df = pd.DataFrame(time_names, columns=['name'])
fillers = ['the', 'a', 'an', 'and', 'or', 'but', 'if', 'then', 'that', 'which', 'who', 'whom',
           'whose', 'what', 'where', 'when', 'why', 'how', 'so', 'such', 'very', 'too',
           'just', 'only', 'even', 'also', 'still', 'yet', 'already', 'still', 'again',
           'back', 'forth', 'here', 'there', 'everywhere', 'anywhere', 'nowhere', 'somewhere',
           'anyone', 'everyone', 'someone', 'no one', 'nothing', 'everything', 'something',
           'anything', 'everything', 'something', 'nothing', 'nobody', 'everybody', 'somebody',
           'anybody', 'everybody', 'somebody', 'nobody', 'each', 'every', 'all', 'both', 'there',
           'though', 'although', 'even though', 'despite', 'in spite of', 'because', 'since',
           'either', 'neither', 'whether', 'while', 'as', 'like', 'such as', 'for example',
           'good', 'bad', 'great', 'awesome', 'fantastic', 'terrible', 'horrible',
           'amazing', 'wonderful', 'excellent', 'poor', 'mediocre',
           'interesting', 'would', 'will', 'shall', 'can', 'could', 'may', 'might',
           'must', 'should', 'ought to', 'need to', 'have to',
           'want to', 'like to', 'love to', 'hate to', 'prefer', 'known', 'dozen', 'founded', 'want', 'closing', 'leader',
           'institute', 'college', 'university', 'school', 'campus', 'program', 'department',
           'faculty', 'student', 'staff', 'administration', 'board', 'trustees', 'president',
           'chancellor', 'dean', 'director', 'office', 'center', 'institute', 'program', 'major',
           'minor', 'course', 'class', 'degree', 'diploma', 'certificate', 'transcript', 'going', 'system', 'continue', 'continuing',
           'announcement', 'announcement', 'announced', 'announces', 'announcing', 'said', 'says', 'report', 'reports',
           'higher', 'saint', 'challenge', 'commitment', 'work', 'point', 'operate', 'prior', 'similar', 'people', 'merger',
           'trustee', 'federal', 'graduate', 'statement', 'close', 'including', 'accreditation', 'accredited', 'accrediting', 'accreditation',
           'include', 'many', 'recent', 'recently', 'undergraduate', 'graduate', 'last', 'transfer', 'official', 'officials', 'number', 'spring', 'future',
           'cut', 'fall', 'summer', 'forward', 'science']
fillers_df = pd.DataFrame(fillers, columns=['name'])

stop_words = set(stopwords.words('english'))
custom_stop_words = {'university', 'read', 'subscribe', 'click', 
                        'newsletter', 'email', 'reported', 'said',
                        'says', 'report', 'according', 'college',
                        'island', 'staten', 'state', 'evans', 'notre', 'dame', 'martin', 'uwoshkosh',
                        'berg', 'louis', 'school', 'campus', 'college', 'university', 'robert', 'johnson', 'see', 
                        'increasing', 'decreasing', 'declining', 'rise', 'fall', 'growth', 'decline', 'trend',
                        'vice', 'hope', 'located', 'location', 'john', 'option', 'one', 'detail', 'joint',
                        'saying', 'dollar', 'planned', 'letter', 'comission', 'commission', 'commissioner', 'education', 'institution', 'institutions'
                        'population', 'condition', 'change', 'increase', 'standard', 'resource', 'family', 'several', 'mission', 'agreement', 'pressure', 'agreement',
                        'institutional', 'institutionally', 'institution', 'institutions', 'institutionalized', 'institutionalizing', 'institutionalism', 'institutionalize',
                        'institutionalized', 'institutionalizes', 'institutionalizing', 'institutional', 'available', 'need', 'offer', 'tried', 'early',
                        'position', 'almost', 'expected', 'didnt', 'did', 'doesnt', 'does', 'dont', 'do', 'doing', 'done',
                        'go', 'going', 'gone', 'get', 'getting', 'got', 'gotten', 'gotta', 'gonna', 'gonna', 'gonna',
                        'gonna', 'gonna', 'gonna', 'come', 'enrolled', 'longer', 'wrote', 'administrator', 'cited', 'employee', 'committed', 'job', 'jobs', 'small', 'two', 'plan',
                        'following', 'opportunity', 'opportunities', 'opportunity', 'opportunistic', 'opportunistically', 'opportunist', 'opportunists',
                        'body', 'reach', 'area', 'decade', 'decade', 'years', 'year', 'yearly', 'annual', 'annually',
                        'failed', 'closure', 'operating', 'million', 'time', 'offering', 'well', 'development', 'development', 'developed', 'developing', 'develops',
                        'ensure', 'create', 'best', 'pay', 'possible', 'goal', 'create', 'partnership', 'partnerships', 'partner', 'partners',
                        'recently', 'decision', 'association', 'process', 'door', 'operation', 'larger', 'end', 'shut', 'transition', 'county',
                        'make', 'especially', 'loss', 'better', 'net', 'business', 'businesses', 'businessman', 'building', 'impact', 'make', 'especially',
                        'factor', 'fell', 'much', 'longterm', 'needed', 'providing', 'provide', 'provides', 'provided', 'providing', 'provides',
                        'member', 'right', 'spokesperson', 'spokespeople', 'spokespersons', 'spokeswoman', 'spokesman', 'spokespeople',
                        'look', 'meet', 'community', 'within', 'academic', 'current', 'past', 'local', 'coming', 'among', 'data', 'fouryear', 'four', 'year', 'rate', 'among',
                        'population', 'first', 'deal', 'name', 'took', 'making', 'teachout', 'began', 
                        'study', 'together', 'information', 'website', 'team', 'final', 'ago', 'day', 'significant'}
custom_stop_words.update(college_df.str.lower().tolist())
custom_stop_words.update(location_df['name'].str.lower().tolist())
custom_stop_words.update(time_df['name'].str.lower().tolist())
custom_stop_words.update(fillers_df['name'].str.lower().tolist())
stop_words.update(custom_stop_words)

def preprocess_text(text):
    if not isinstance(text, str) or not text.strip():
        return []
    
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    tokens = [token for token in tokens if token not in stop_words]
    tokens = [token for token in tokens if len(token) > 2 and len(token) < 20]
    tokens = [token for token in tokens if not token.isdigit()]
    tokens = [token for token in tokens if token.isalpha()]

    return tokens

dfc = df.copy()
dfc['tokens'] = dfc['content'].apply(preprocess_text)

dictionary = Dictionary(dfc['tokens'])
dictionary.filter_extremes(no_below=7, no_above=0.9)
corpus = [dictionary.doc2bow(text) for text in dfc['tokens']]

dfc.to_csv("processed_article_content.csv", index=False)
dictionary.save("article_dictionary.gensim")

tfidf = TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

with open("corpus_tfidf.pkl", "wb") as f:
    pickle.dump(corpus_tfidf, f)