import re
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras import Sequential
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Dense
from threading import Thread
from Components.DispatcherStore import DispatcherStore
from config import API_KEY
from polygon import StocksClient

class Engine(Thread):
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.close = self.get_close_price()
        self.model = None
        self.consumer = DispatcherStore.createPolygonDataDispatcherConsumer(key=self.symbol)
        self.new_close = None
        self.historical_signal = DispatcherStore.createPolygonDataDispatcherProducer()

    def __get_historical_data(self):
        return pd.read_csv(f"Historical Data/{self.symbol}")

    def __normalization(x):
        return (x-min(x)/max(x)-min(x)) 

    def get_close_price(self):
        raw_data = self.__get_historical_data()
        stock_prices = raw_data.close.values.astype('float32')
        stock_prices = stock_prices.reshape(len(stock_prices), 1)
        return self.__normalization(stock_prices)

    def __train_test_split(stock):
        train_size = int(len(stock) * 0.80)
        test_size = len(stock) - train_size
        train, test = stock[0:train_size,:], stock[train_size:len(stock),:]
        return train, test
    
    def create_dataset(dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return np.array(dataX), np.array(dataY)
    
    def create_trainTest(self):
        train, test = self.__train_test_split(self.close)                 
        # reshape into X=t and Y=t+1
        look_back = 1
        trainX, trainY = self.create_dataset(train, look_back)
        testX, testY = self.create_dataset(test, look_back)
        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
        return trainX, testX, trainY, testY
    
    def first_train(self):
        trainX, testX, trainY, testY = self.create_trainTest()
        model = Sequential()
        model.add(LSTM(units=50,return_sequences=True,input_shape=(trainX.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50,return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50,return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
        model.compile(optimizer='adam',loss='mean_squared_error')
        model.fit(trainX, trainY,epochs=15,batch_size=32)
        results = model.evaluate(testX, testY, batch_size=32)
        print("test loss, test MSE:", results)
        return model
    
    def new_trainTest():
        """
        This function will flow in the new data and preprocess it
        """
        return None

    def re_train(self, model):
        new_trainX, new_trainY, new_testX, new_testY = self.new_trainTest()
        model.save('test1.h5')
        model1 = tf.keras.models.load_model('test1.h5')
        model = Sequential([model1])
        model.compile(optimizer='adam',loss='mean_squared_error') 
        model.fit(new_trainX, new_trainY, epochs = 15, batch_size=32)
        results = model.evaluate(new_testX, new_testY, batch_size=32)
        print("test loss, test MSE:", results)
    


    def main():
        model = first_train()
        for i in range(0,5):
            re_train(model)