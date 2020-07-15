import tweepy  #manage the authentication to the API through our secret keys
import datetime
import requests
import os
import random
import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

from selenium import webdriver  
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


consumer_key = 'XXX'
consumer_secret = 'XXX'

access_token = 'XXX'
access_token_secret = 'XXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)          #where we store auth settings



class Stock:
    def __init__(self, url, name):
        self.url = url;
        self.name = name;
        self.number = 0
        self.percent = 0
        



def publictweet():

    snp_URL = 'https://finance.yahoo.com/quote/%5EGSPC?p=^GSPC'
    dow_URL = 'https://finance.yahoo.com/quote/%5EDJI?p=^DJI'
    nasdaq_URL = 'https://finance.yahoo.com/quote/%5EIXIC?p=^IXIC'
    russell_URL = 'https://finance.yahoo.com/quote/%5ERUT?p=^RUT'

    SnP = Stock(snp_URL, "SnP")
    Dow = Stock(dow_URL, "Dow")
    Nasdaq = Stock(nasdaq_URL, "Nasdaq")
    Russell = Stock(russell_URL, "Russell")

    
    indexes = [SnP, Dow, Nasdaq, Russell]

    for stock in indexes:
        page = requests.get(stock.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        temp1 = soup.find(id='app').find(id='quote-header-info')

        result = temp1.find_all("span", class_="Trsdu(0.3s) Fw(500) Fz(14px) C($positiveColor)")
        if (len(result) == 0):
            result = temp1.find_all("span", class_="Trsdu(0.3s) Fw(500) Fz(14px) C($negativeColor)")
        
        for data in result:
            data1 = data.text.split()
            number = float(data1[0][0:-1])
            percent = float(data1[1][1:-2])
            stock.number = number
            stock.percent = percent


    tweet = "Today's Market Results:\n\n"
    for x in indexes:
        tweet += x.name + ": " + str(x.number) + " (" + str(x.percent) + '%)\n'

    tweet = tweet + '#stocks #stockmarket #nasdaq #russell2000 #dowjones #sp500'
    print(tweet)


    #predict mood
    total = 0.0
    for stock in indexes:
        total += percent


    negative = ['concerned', 'surprised', 'shock', 'fear', 'scared']
    neutral = ['not bad', 'ok then', 'eh', 'suspicious']
    positive = ['nice', 'good', 'awesome', 'celebrate']
    

    if (total > 4.0):
        num = random.randint(2,3)
        q = positive[num]
        
    elif (total > 2.5):
        num = random.randint(0,1)
        q = positive[num]
        
    elif (2.5 > total > 0):
        num = random.randint(2,3)
        q = neutral[num]
        
    elif (0 > total > -2.5):
        num = random.randint(0,1)
        q = neutral[num]
        
    elif (total < -2.5):
        num = random.randint(0,2)
        q = negative[num]

    elif (total < -4.0):
        num = random.randint(2,4)
        q = negative[num]
    

    
    #find gif
    api_instance = giphy_client.DefaultApi()
    api_key = 'AwivSuLAzc432ktTJEm0GK77L9mGBcTx'
    #q = 'happy'
    limit = 20
    offset = 0
    rating = 'g'
    lang = 'en'
    fmt = 'json'

    try:
        api_response = api_instance.gifs_search_get(api_key, q, limit=limit, offset=offset, rating=rating, lang=lang, fmt=fmt)
        gif_choice = random.randint(0,limit-1)
        print(gif_choice)
        data = api_response.data[gif_choice]
        gif_id = data.id

        
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

        

    #set gif
    url  = 'https://media.giphy.com/media/{}/giphy.gif'.format(gif_id)
    print(url)
    filename = 'mood.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=tweet)
        #os.remove(filename)
    else:
        print("unable to download image")


publictweet()



