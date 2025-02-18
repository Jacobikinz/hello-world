# -*- coding: utf-8 -*-
"""SimpleNewsGraphs v2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1db7xDe9ToxbQKVq6STtJJdk893RzA3Tg

# RSS Live Feed to Pandas
"""

!pip install feedparser

from sklearn import cluster, datasets
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csv
from sklearn.model_selection import train_test_split
import random

"""**Creating RSS news list**"""

import feedparser

#news sources to import fromt 
newsurls = {
    'apnews':           'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305',
    'googlenews':       'https://news.google.com/news/rss/?hl=en&amp;ned=us&amp;gl=US',
    'yahoonews':        'http://news.yahoo.com/rss/',
    'cbnc':             'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    'espn':             'http://www.espn.com/espn/rss/news',
    'nytimes_environment':  "http://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml",
    'nytimes_business':     "http://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    'nytimes_economy':      "http://rss.nytimes.com/services/xml/rss/nyt/Economy.xml",
    'nytimes_dealbook':     "http://rss.nytimes.com/services/xml/rss/nyt/Economy.xml",
}

#(hopefully) continuously building dataset
data = pd.DataFrame()

#add something useful to the dataframe!!
for key,url in newsurls.items():
  feed = feedparser.parse(url)
  rawData = pd.DataFrame.from_dict(feed['items'])
  data = pd.concat([data, rawData], sort=True)

"""# Sentiment Analysis"""

from datetime import datetime

#yay I'm solving my life problems by creating excessive PANDAS frames
headlines = pd.DataFrame()

headlines['title'], headlines['time_raw'] = data['title'], data['published_parsed'] #lol see

import time as ti
output = []
for val in headlines['time_raw'].values:
    output.append(ti.strftime("%Y-%m-%d %H:%M:%S", val))
       
headlines['fixed_time'] = output

#sentiment stuff!

import nltk
nltk.download('vader_lexicon')

def nltk_sentiment(sentence):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    nltk_sentiment = SentimentIntensityAnalyzer()
    score = nltk_sentiment.polarity_scores(sentence)
    return score
  
sentiment_raw = headlines['title'].apply(nltk_sentiment)
sentiment = pd.DataFrame(sentiment_raw.values.tolist())

headlines['stringTime'] = headlines['fixed_time']
headlines['stringTime'].replace(regex=True,inplace=True,to_replace=r'-',value=r'')
headlines['stringTime'].replace(regex=True,inplace=True,to_replace=r'\:',value=r'')
headlines['stringTime'].replace(regex=True,inplace=True,to_replace=r' ',value=r'')

numericalHeadline = sentiment.iloc[:,0]
time = headlines.iloc[:,-2]

headlines
headlines.to_csv('headliners.csv')
plt.scatter(time, numericalHeadline)

headlines

"""#Getting Minute-by-Minute Data
https://www.cloudsigma.com/nasdaq-per-minute-data-using-python/
"""

import urllib.request
import json
import os

def import_web(ticker):
    """
    :param identifier: List, Takes the company name
    :return:displays companies records per minute
    """
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker +'&interval=1min&apikey=' + 'LIH75FGJ5OL2MJSZ' + '&outputsize=full&datatype=json'
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr


def get_value(ticker):
    js = import_web(ticker)
    parsed_data = json.loads(js) # loads the json and converts the json string into dictionary
    ps = parsed_data['Time Series (1min)']
    partitionSave(ps,ticker)

            
def partitionSave(ps,ticker):
    date = {}
    for i in ps:
        date[i[:10]] = "date"
    for d in date.keys():
        tmp = {}
        for i in ps:
            if(i[:10] == d):
                tmp[i] = ps[i]
        if(os.path.isdir(d) == False):
            os.mkdir(d)
        fname = ticker + "_dann"
        try:
            with open(os.path.join(d,fname),'r') as f:
                t = json.load(f)
                for i in t:
                    tmp[i]=t[i]
        except Exception as e:
            pass
                
        with open(os.path.join(d,fname), 'w') as f:
            json.dump(tmp, f)
                
def main():
    #Start Process
    company_list = ['GOOGL','MSFT','ORCL','FB','AAPL','TSLA'];
    try:
        for company in company_list:
            print("Starting with " + company)
            get_value(company)
            print("Ended Writing Data of " + company)
    except Exception as e:
        print(e)

main()

cd /content/

from pandas.io.json import json_normalize
import datetime

#def dataToPandas(ticker, date):

today = datetime.date.today()  
todayday = today.day

filenamer = "2019-05-%s/AAPL_dann" % todayday


with open(filenamer) as f:
	 parseData_raw = json.load(f)

for key in parseData_raw:
	temp={}
	parseData=parseData_raw[key]
	for key2 in parseData:
		temp[key2[3:]]=float(parseData[key2])
	parseData_raw[key]=temp
  
stockDataCompany = pd.DataFrame(parseData_raw).transpose()

stockDataCompany = stockDataCompany.reset_index()
stockDataCompany['openToClose'] = stockDataCompany['open']-stockDataCompany['close']

stockDataCompany

#stockDataCompany['index'].replace(regex=True,inplace=True,to_replace=r'-',value=r'')
#stockDataCompany['index'].replace(regex=True,inplace=True,to_replace=r'\:',value=r'')
#stockDataCompany['index'].replace(regex=True,inplace=True,to_replace=r' ',value=r'')

headlines[3:10]

sentiment[3:10]

"""https://www.datacamp.com/community/tutorials/joining-dataframes-pandas"""

print (headlines.shape)
print (sentiment.shape)

headlines['compound'] = sentiment['compound']
headlines['neg'] = sentiment['neg']
headlines['neu'] = sentiment['neu']
headlines['pos'] = sentiment['pos']

print (headlines.iloc[0])
#print (headlines)
headlines[0:10]["stringTime"]

stockDataCompany[0:10]["index"]

#headlines

data0 = pd.concat([sentiment, headlines], sort=True, axis=1)
data0

data = pd.concat([sentiment, stockDataCompany], sort=True, axis=1)

data = pd.DataFrame.dropna(data)
data

data.to_csv('stock_minutes.csv')

import datetime 

currentTime = datetime.datetime.now()
currentTime = str(currentTime)

year = currentTime[0:4]
month = currentTime[5:7]
day = currentTime[8:10]


def openStock(ticker):
  for i in range(5):
    currentDay = int(day)-i
    with open(+year+'-'+month+'-'+day+'/'+ticker+'_dann') as f:
	    parseData_raw = json.load(f)

    for key in parseData_raw:
	    temp={}
	    parseData=parseData_raw[key]
	    for key2 in parseData:
		    temp[key2[3:]]=float(parseData[key2])
	    parseData_raw[key]=temp
  
  stockDataCompany = pd.DataFrame(parseData_raw).transpose()
  
  return stockDataCompany

plt.figure()
plt.scatter(data["index"], data["openToClose"])
plt.scatter(data["index"], data["compound"])

"""#LINEAR REGRESSION"""

train, test = train_test_split(data, test_size=0.2)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
linregtest = LinearRegression(normalize=True)

X = train.loc[:,"compound"].values.reshape(-1,1)
y = train.loc[:,'openToClose']

linregtest.fit(X, y)
predicted_close = linregtest.predict(test["compound"].values.reshape(-1,1))

plt.figure()
plt.plot(test["compound"], predicted_close)
plt.scatter(test["compound"], test["openToClose"])

"""#NEURAL NET"""

from sklearn.neural_network import MLPRegressor

neuralnet = MLPRegressor()
neuralnet.fit(X, y)

predicted_close = neuralnet.predict(test["compound"].values.reshape(-1,1))

plt.figure()
plt.plot(test["compound"], predicted_close)
plt.scatter(test["compound"], test["openToClose"])

