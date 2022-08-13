from xml.etree.ElementInclude import DEFAULT_MAX_INCLUSION_DEPTH
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from threading import Thread
import threading
from Components.DispatcherStore import DispatcherStore
from config import API_KEY
from time import sleep
import pymongo

class Engine(Thread):
    def __init__(self, symbol: str):
        self.plot_path = "../stock_web/src/forecast_image"
        self.n_lookback = 60  # length of input sequences (lookback period)
        self.n_forecast = 30  # length of output sequences (forecast period)
        client = pymongo.MongoClient("mongodb+srv://hungduonggia181:Tiberiumwars123@summerproject.sgjfjf9.mongodb.net/?retryWrites=true&w=majority")
        db = client["stock-data"]
        self.db_collection = db[f"forecast-{symbol}"]
        self.stock = None
        self.scaler = None
        self.symbol = symbol
        self.model = None
        self.historical_signal = DispatcherStore.createHistoricalSignalProducer(key=self.symbol)
        self.new_close = None
        self.historical_data = None
        self.new_realtime_data = None
        self.data_id = None
        self.historical_data_listner = threading.Thread(target=self.create_historical_data_consumer, args=())
        self.historical_data_listner.start()
        self.realtime_data_listener = threading.Thread(target=self.create_realtime_data_consumer, args=())
        self.realtime_data_listener.start()
        sleep(0.1)

        self.run()

    def create_realtime_data_consumer(self):
        realtime_consumer = DispatcherStore.createModelConsumer(key=f'realtime_{self.symbol}', callback=self.preprocess_realtime_data)
    
    def create_historical_data_consumer(self):
        historical_consumer = DispatcherStore.createModelConsumer(key=f'hist_{self.symbol}', callback=self.start_predict_stock)

    def set_new_realtime_data(self, data):
        self.new_realtime_data = data 
    
    def __get_historical_data(self):
        return self.historical_data

    def __set_historical_data(self, data):
        
        self.historical_data = data

    def preprocess_historical_data(self, data):
        raw_data = data["data"]
        df = pd.DataFrame(eval(raw_data))
        df["date"] = pd.to_datetime(df["date"], unit="ms")
        df = df.iloc[::-1] 
        df.drop(index=0)
        self.__set_historical_data(df)

    def preprocess_realtime_data(self, data):
        self.set_new_realtime_data(pd.DataFrame(eval(data["data"])))

    def __get_scaler(self):
        return self.scaler
    
    def __get_stock(self):
        return self.stock
    
    def __set_scaler(self, scaler):
        self.scaler = scaler
    
    def __set_stock(self, stock):
        self.stock = stock
    
    def __get_data_id(self):
        return self.data_id
    
    def __set_data_id(self, new_data_id):
        self.data_id = new_data_id

    def generate_scaler_stock(self):
        df = self.__get_historical_data()
        scaler = MinMaxScaler(feature_range=(0, 1))
        y = df['close']
        y = y.values.reshape(-1,1)
        scaler = scaler.fit(y)
        y = scaler.transform(y)
        self.__set_stock(y)
        self.__set_scaler(scaler)
        # return y, scaler
    
    # # stock, scaler = preprocess(df)

    def generate_XY(self, stock):
        """
        This function will generate X,Y as X train and Y train
        Will be modified to be updated regularly
        """
        X = []
        Y = []

        for i in range(self.n_lookback, (len(stock)) - self.n_forecast + 1):
            X.append(stock[i - self.n_lookback: i])
            Y.append(stock[i: i + self.n_forecast])

        X = np.array(X)
        Y = np.array(Y)
        return X,Y
    
    def train(self,X,Y):
        """
        Train model
        """
        np.random.seed(1234)
        tf.random.set_seed(1234)
        model = Sequential()
        model.add(LSTM(units=30,return_sequences=True,input_shape=(self.n_lookback, 1), activation = 'relu'))
        model.add(LSTM(units=30,return_sequences=True, activation = 'relu'))
        model.add(LSTM(units=30,return_sequences=True, activation = 'relu'))
        model.add(LSTM(units=30, activation = 'relu'))
        model.add(Dense(self.n_forecast))
        model.compile(optimizer='adam',loss='mean_squared_error')
        model.fit(X, Y,epochs=100,batch_size=32)
        model.summary()
        model.save('future.h5')

    def run_train(self, stock): #run this to train the dataset 
        """
        Run the TRAINING algorithm on the historical data
        """
        X_,Y_ = self.generate_XY(stock)
        self.train(X_,Y_)
    
    def gen_forecasts(self, stock):
        """
        Generate forecasts from the updated model
        @stock: preprocessed stock variable
        @return: Y_ the forecast prices for the next 30 days
        """
        scaler = self.__get_scaler()
        model = tf.keras.models.load_model('future.h5')

        X_ = stock[-self.n_lookback:]  # last available input sequence
        X_ = X_.reshape(1, self.n_lookback, 1)

        Y_ = model.predict(X_).reshape(-1, 1)
        Y_ = scaler.inverse_transform(Y_)

        return Y_
    
    """Data frame of the forecasts
    #Append two of them to the variable results
    Plot both
    """
    def gen_dfPast(self, df):
        df_past = df[['close']]
        df_past['date'] = pd.to_datetime(df['date'])
        df_past['forecast'] = np.nan
        return df_past

    def gen_dfFuture(self, df_past, forecast):
        df_future = pd.DataFrame(columns=['close', 'date', 'forecast'])
        df_future['date'] = pd.date_range(start=df_past['date'].iloc[-1] + pd.Timedelta(minutes=1), periods=self.n_forecast)
        df_future['forecast'] = forecast.flatten()
        results = df_past.append(df_future).set_index('date')
        return results, df_future

    def plot_pred(results):
        plt.figure(figsize=(16,6))
        plt.title('30 days predictions')
        plt.plot(results)
        #Uncomment this when real-time is fully implemented
        plt.savefig('real1.png', dpi = 300, bbox_inches = 'tight')
    
    def plot_pred2(df_future):
        future = df_future.set_index('date') 
        future.plot()
    
    def predict(self):
        
        forecast = self.gen_forecasts(self.__get_stock())
       
        dfPast = self.gen_dfPast(self.__get_historical_data())
        
        results, dfFuture = self.gen_dfFuture(dfPast, forecast)
        plt.figure(figsize=(16,6))
        plt.title('30 days predictions')
        plt.plot(results)
        #Uncomment this when real-time is fully implemented
        plt.savefig(f'{self.plot_path}/real1-{self.symbol}.png', dpi = 300, bbox_inches = 'tight')
        future = dfFuture.set_index('date') 
        plt.plot(future)
        plt.savefig(f'{self.plot_path}/real2-{self.symbol}.png', dpi = 300, bbox_inches = 'tight')
        dfFuture = dfFuture.drop(columns=["close"])
        db_data = {"forecast_id": self.__get_data_id(), "forecast": dfFuture.to_dict('records')}
        self.db_collection.insert_one({"results": db_data})
        print("data inserted")

    def start_predict_stock(self, data):
        self.__set_data_id(data["id"])
        print(f"Here is data id for {self.symbol}: ", data["id"])
        self.preprocess_historical_data(data)
        self.generate_scaler_stock()
        self.run_train(self.__get_stock())
        self.predict()
            
    def run(self):
        while True:
            sleep(5)