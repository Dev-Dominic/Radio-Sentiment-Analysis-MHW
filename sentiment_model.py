import pandas as pd
import numpy as np

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk.collocations import *
import string
from textblob import TextBlob
from nltk import tokenize
from nltk.corpus import stopwords, gutenberg
from wordcloud import WordCloud
from nltk.tokenize import regexp_tokenize, word_tokenize, RegexpTokenizer

import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
import seaborn as sns

# loading data
df = pd.read_csv('jamaican_news.csv')

# manually updating incorrect info
df['Link'][1] = 'https://jamaica.loopnews.com/content/sagicor-financial-announces-retirement-dodridge-miller'
df['Date'][1] = '01/26/2023'
df['Date'][0] = '01/28/2023'
df['Date'][3] = '09/26/2022'

# lowercase
df.Text = [txt.lower().strip() for txt in df.Text]
df.Title = [txt.lower().strip() for txt in df.Title]

# converting date to correct format
df.Date = [pd.to_datetime(day) for day in df.Date]

# function to calculate polarity of text
def get_polarity(text):
    return TextBlob(text).sentiment.polarity

# getting polarity scores for each article
df['Polarity'] = df['Text'].apply(get_polarity)

# plotting a histogram of polarity
df['Polarity'].hist()

# used median, std dev to determine thresholds
df['Sentiment_Type'] = ''
df.loc[df.Polarity>0.09,'Sentiment_Type'] = 'POSITIVE'
df.loc[(df.Polarity>=0.05) & (df.Polarity<=0.09), 'Sentiment_Type'] = 'NEUTRAL'
df.loc[df.Polarity<0.05,'Sentiment_Type'] = 'NEGATIVE'

# plotting histogram of Sentiment values
df.Sentiment_Type.value_counts().plot(kind='bar',title="Sentiment Analysis")

# tokenizing with regex tokenizer
basic_token_pattern = r"(?u)\b\w\w+\b"
tokenizer = RegexpTokenizer(basic_token_pattern)

# Create new column with tokenized data
df["text_tokenized"] = df["Text"].apply(tokenizer.tokenize)

# storing stopwords list and adding punctuation
stopwords_list = stopwords.words('english')
stopwords_list += list(string.punctuation)

# function to remove stopwords
def remove_stopwords(token_list):
    """
    Given a list of tokens, return a list where the tokens
    that are also present in stopwords_list have been
    removed
    """
    return [word for word in token_list if word not in stopwords_list]

# applying remove stopwords function
df["text_without_stopwords"] = df["text_tokenized"].apply(remove_stopwords)

# function to generate word cloud for a company
def gen_wordcloud(company):
    
    wordcloud = WordCloud(max_words = 200, stopwords = None, 
                          collocations = False, width = 600, height = 400, 
                          background_color = 'white', 
                          colormap = 'plasma') 

    wordcloud.generate(",".join(df["text_without_stopwords"]\
                                [df['Company']==company].explode())) 

    plt.figure(figsize = (7, 7), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.title('Sagicor Word Cloud', fontsize=15)
    plt.savefig(f'images/{company}_wordcloud.png')
    
# list of companies
companies = list(set(df.Company))

# generate wordcloud
for company in companies:
    gen_wordcloud(company)
    
# function to plot sentiment over time    
def plot_sentiment(company):
    
    plt.style.use('ggplot')
    
    fig, ax = plt.subplots(figsize = (8, 5))
    sns.lineplot(data=df[df.Company==company], x="Date", y="Polarity")
    
    plt.title(f'{company} Sentiment', fontsize=15)
    plt.xticks(rotation=45)
    myFmt = mdates.DateFormatter('%b %Y') 
    ax.xaxis.set_major_formatter(myFmt)
    
    plt.savefig(f'images/{company}_sentiment_timeseries.png')
    
# plot sentiment    
for company in companies:
    plot_sentiment(company)