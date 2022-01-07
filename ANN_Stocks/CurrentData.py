import requests
import time
import re
import copy
import os
import asyncio
import aiohttp
import numpy as np
from datetime import datetime

date = datetime.today().strftime('%m-%d-%y')
backupFile = open(f"CurrentData.csv", "w+")
backupFile.write("Ticker,Price,Analysts,Buy,Overweight,Hold,Sell,Lowcast,Forecast,Highcast\n")

nasdaqFile = open("nasdaqFile.txt", "w+")
nyseFile = open("nyseFile.txt", "w+")
os.system("bash ./nasdaq.sh > nasdaqFile.txt")
os.system("bash ./nyse.sh > nyseFile.txt")

nasdaqList = nasdaqFile.readlines()
nyseList = nyseFile.readlines()
symbolDict = {}
symbolNum = 0

for line in range(len(nasdaqList)):
    nasdaqList[line] = nasdaqList[line].split(" ")
    symbolDict[nasdaqList[line][0]] = "NASDAQ"

for line in range(len(nyseList)):
    nyseList[line] = nyseList[line].split(" ")
    if (nyseList[line][2] == "N"):
        symbolDict[nyseList[line][0]] = "NYSE"

async def main(symbolDict):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for ticker in symbolDict.keys():
            url = f"https://www.marketbeat.com/stocks/{symbolDict[ticker]}/{ticker}/price-target/"
            task = asyncio.create_task(fetch(session, url, ticker))
            tasks.append(task)

        await asyncio.gather(*tasks)

async def fetch(session, url, ticker):
    try:
        async with session.get(url) as resp:
            text = await resp.text()
            await scrape(text, ticker)
    except:
        pass

async def scrape(text, ticker):
    global symbolNum
    try:
        MarketSource = text.replace("\n","").replace(" ","").replace(",","")
        price = float(re.search("'price'><strong>\$([0-9]+\.[0-9]*)</strong>", MarketSource).group(1))
        
        lowcast = round(float(re.search(f"LowPT</th><tdclass='text-right'>\$([0-9]+\.[0-9]*)", MarketSource).group(1))/price - 1, 2)
        forecast = round(float(re.search(f"AveragePT</th><tdclass='text-right'>\$([0-9]+\.[0-9]*)", MarketSource).group(1))/price - 1, 2)
        highcast = round(float(re.search(f"HighPT</th><tdclass='text-right'>\$([0-9]+\.[0-9]*)", MarketSource).group(1))/price - 1, 2)

        CurrentRatings = re.search("bg\-dark\-green(.*)ConsensusPriceTarget",MarketSource).group(1)
        CurrentRatingsList = re.findall(">([0-9]+|N/A)<", CurrentRatings)
        Buy = int(CurrentRatingsList[0])
        Overweight = int(CurrentRatingsList[4])
        Hold = int(CurrentRatingsList[8])
        Sell = int(CurrentRatingsList[12])
        analysts = Buy + Overweight + Hold + Sell
        '''
        Buy /= float(analysts)
        Overweight /= float(analysts)
        Hold /= float(analysts)
        Sell /= float(analysts)
        '''
        data = (f"{ticker},{price},{analysts},{Buy},{Overweight},{Hold},{Sell},{lowcast},{forecast},{highcast}")
        backupFile.write(f"{data}\n")
        symbolNum += 1
        print(f"{symbolNum}: {data}")

    except:
        pass

asyncio.run(main(symbolDict))  
backupFile.close()

