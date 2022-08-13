from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
import json
from Components.DispatcherStore import DispatcherStore
import uuid
from flask import request
from hashlib import md5
from time import sleep
from json import loads
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

client = MongoClient("mongodb+srv://hungduonggia181:Tiberiumwars123@summerproject.sgjfjf9.mongodb.net/?retryWrites=true&w=majority")
db = client["stock-data"]


class check_alive(Resource):
    def get(self):
        return {"status": 200, "Message": "Backend Alive"}

class get_forecast_historical_data(Resource):
    def post(self):
        json_request_data = request.get_json()
        symbol = json_request_data["symbol"]
        historical_signal = DispatcherStore.createHistoricalSignalProducer(key=symbol)
        uuid_id = str(uuid.uuid4())
        historical_signal.send({"signal": "get_most_recent_historical_data", "id": uuid_id})
        collection = db[f"forecast-{symbol}"]
        while True:
            if collection.find_one({"results.forecast_id": uuid_id}) != None:
                break
            sleep(1)
        response = collection.find_one({"results.forecast_id": uuid_id})["results"]
        if response != None:
            return {"status": 200, "success": True, "data": json.dumps(response, default=str)}
        else:
            return {"status": 400, "success": False, "message": f"There Is No Forecast {uuid_id} Exists."}

api.add_resource(get_forecast_historical_data, '/train_historical')
api.add_resource(check_alive, '/')



if __name__ == '__main__':
    app.run(debug=True)
   
  