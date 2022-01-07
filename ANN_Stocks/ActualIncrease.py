from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

priceHistoryFile = open("fh_5yrs.csv","r")
priceHistory = priceHistoryFile.readlines()
priceHistory.pop(0)

analystHistoryFile = open("analystBackup.csv", "r")
analystHistory = analystHistoryFile.readlines()

trainingDataFile = open("trainingData.csv","w")
trainingDataFile.write("Symbol,Date,Price,Analysts,StrongBuy,Buy,Hold,Sell,Lowcast,Forecast,Highcast,Actual\n")

priceDict = {}

for i in range(len(priceHistory)):
    priceHistoryArr = priceHistory[i].replace("\n","").split(",")
    priceHistory[i] = priceHistoryArr
    SymbolDate = f"{priceHistoryArr[7]}{priceHistoryArr[0]}"
    priceDict[SymbolDate] = float(priceHistoryArr[2])

#priceNP = np.array(priceHistory)
#priceDF = pd.DataFrame(priceNP, columns = ["Date","Volume","Open","High","Low","Close","AdjClose","Symbol"])
#print(priceDF)

print("Begin Process")
for i in range(len(analystHistory)):
    analystHistoryArr = analystHistory[i].replace("\n","").split(",")
    oldDate = datetime.strptime(analystHistoryArr[1], "%m/%d/%Y")
    newDate = oldDate + relativedelta(months=+2)
    oldDate = oldDate.strftime("%Y-%m-%d")
    newDate = newDate.strftime("%Y-%m-%d")
    
    try:
        previousPrice = priceDict[f"{analystHistoryArr[0]}{oldDate}"]
        newPrice = priceDict[f"{analystHistoryArr[0]}{newDate}"]
        actualIncrease = round(newPrice/previousPrice - 1, 4)
        analystHistoryArr[2] = str(previousPrice)
        '''
        analystHistoryArr[4] = str(int(analystHistoryArr[4]) / float(analystHistoryArr[3]))
        analystHistoryArr[5] = str(int(analystHistoryArr[5]) / float(analystHistoryArr[3]))
        analystHistoryArr[6] = str(int(analystHistoryArr[6]) / float(analystHistoryArr[3]))
        analystHistoryArr[7] = str(int(analystHistoryArr[7]) / float(analystHistoryArr[3]))
        '''
        data = f"{','.join(analystHistoryArr)},{actualIncrease}\n"
        trainingDataFile.write(data)
        print(data)
    except:
        pass
            
priceHistoryFile.close()
analystHistoryFile.close()
trainingDataFile.close()


    
