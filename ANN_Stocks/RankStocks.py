import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import load_model

dfTrain = pd.read_csv("trainingData.csv")
dfTrain = dfTrain[(dfTrain["Forecast"] < dfTrain["Highcast"]) & (dfTrain["Lowcast"] < dfTrain["Forecast"])]
dfTrain = dfTrain[(dfTrain["Highcast"] < 10) & (dfTrain["Analysts"] >= 6)]

X = dfTrain[["Price","Analysts","StrongBuy","Buy","Hold","Sell","Lowcast","Forecast","Highcast"]].values
Y = dfTrain["Actual"].values

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=79)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(X_train)

#=================================================================================================================

df = pd.read_csv("CurrentData.csv")
df = df[(df["Forecast"] < df["Highcast"]) & (df["Lowcast"] < df["Forecast"])]
df = df[(df["Highcast"] < 10) & (df["Analysts"] >= 6)]

stockData = df.values
stockNames = np.reshape(stockData[:,0], (-1, 1))
stockNumbers = scaler.transform(stockData[:,1::])
stockData = np.concatenate((stockNames, stockNumbers), axis=1)
ResultList = []
model = load_model('Stock_Model.h5')
rows = stockData.shape[0]
for i in range(rows):
    stockName = str(stockData[i,0])
    stockInfo = stockData[i, 1::]
    stockInfo = np.asarray(stockInfo).astype('float32')
    print(f"{str(i+1)} out of {str(rows)} - {stockName}")
    expectedIncrease = model.predict([stockInfo.tolist()])[0]
    ResultList.append([stockName, expectedIncrease])

ResultList.sort(key=lambda x:x[1])
ResultList.reverse()
ResultFile = open("Results.txt","w")

for i in ResultList:
    ResultFile.write(str(i) + "\n")

ResultFile.close()