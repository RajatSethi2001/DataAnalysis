import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


df = pd.read_csv("trainingData.csv")
df = df[(df["Forecast"] < df["Highcast"]) & (df["Lowcast"] < df["Forecast"])]
df = df[(df["Highcast"] < 10) & (df["Analysts"] >= 6)]

#=========================================================================================

X = df[["Price","Analysts","StrongBuy","Buy","Hold","Sell","Lowcast","Forecast","Highcast"]].values
Y = df ["Actual"].values

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=79)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation

model = Sequential()
model.add(Dense(9, activation='relu'))
model.add(Dense(9, activation='relu'))
model.add(Dense(9, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='rmsprop',loss='mse')
model.fit(X_train,Y_train,epochs=500)

training_score = model.evaluate(X_train, Y_train) ** 0.5
testing_score = model.evaluate(X_test, Y_test) ** 0.5
print(training_score)
print(testing_score)

from tensorflow.keras.models import load_model
model.save('Stock_Model.h5')