import React, { useState, useEffect } from 'react';
import axios from "axios";
import StockStats from '../Components/StockStats';
import StockGraph from '../Components/StockGraph';
const api = axios.create({
    baseURL: `http://127.0.0.1:5000`,
    headers: {
        "Content-Type": "application/json",
        'Access-Control-Allow-Origin': "*"
    },
})

const StockContainer = (props) => {
    const [isLoading, setLoading] = useState(false)
    const [stock, setStock] = useState([])
    const [display, setDisplay] = useState(false)
    const pathPlot1 = `../forecast_image/real1-${props.symbol}.png`
    const pathPlot2 = `../forecast_image/real2-${props.symbol}.png`

    const fetchForcastHist = async () => {
        console.log("here is props", props)
        setDisplay(false)
        setLoading(true)

        const data = await api.post('/train_historical', 
            {"symbol" : props.symbol})

        const parsedData = JSON.parse(data.data.data)
        console.log(parsedData)
        setStock([...parsedData["forecast"]])
        setLoading(false)
        setDisplay(true)
    }

    return (
        <div className="stock-main-container">
            <div className="stock-container-uppper">
                <div className="stock-container-label">
                    <div>{props.symbol}</div>
                </div>
                <div className="stock-container-button-area">
                    <div>
                        {
                            isLoading? <div>Training</div> : <button onClick={fetchForcastHist}>Predict</button>
                        }
                    </div>
                </div>
            </div>
            <div className="stock-container-lower">
                <div className="stock-container-stats">
                    <div className='stats-header'>Results</div>
                    {
                        isLoading? <div>Training</div> : 
                        <div className='stats-holder'>{stock.map((data, index) => {
                            return (
                                <StockStats date={data["date"]} forecast={data["forecast"]} key={index}/>
                            )
                        })}</div>
                    }
                </div>
                <div className="stock-container-graph">
                    {display?
                    <div>
                        <StockGraph source={pathPlot1}></StockGraph>
                        <StockGraph source={pathPlot2}></StockGraph>
                    </div> :
                    <div>
                    </div>
                    }
                </div>
            </div>
        </div>
    )
}

export default StockContainer;