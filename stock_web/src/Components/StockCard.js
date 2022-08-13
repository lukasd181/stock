import React, { useState, useEffect } from 'react';
import axios from "axios";
import StockStats from './StockStats';

const api = axios.create({
    baseURL: `http://127.0.0.1:5000`,
    headers: {
        "Content-Type": "application/json",
        'Access-Control-Allow-Origin': "*"
    },
})


const StockCard = (props) => {

    // const get_data_api = 
    const [count, setCount] = useState(0);
    const [loading, setLoading] = useState(false)
    const [data, setData] = useState({data: []})

    const [stock, setStock] = useState([])
    
    const fetchData = async () => {
        setLoading(true)
        const promise = await api.get(`/`)
        // console.log(promise)
        setData({data: [promise.data]})
        setLoading(false)
    }

    const fetchForcastHist = async () => {
        console.log("here is props", props)
        setLoading(true)
        const data = await api.post('/train_historical', 
        {
            "symbol" : props.symbol
        })
        const parsedData = JSON.parse(data.data.data)
        setStock([...parsedData["forecast"]])
        setLoading(false)
    }

    // useEffect(() => {
    //     // const dataPromise = promiseParser().then(data => {
    //     //     console.log("data here", data)
    //     // })
        
    //     console.log("ran useEffect")
    //     console.log(promiseParser())


    // //    axios.get('/', {
    // //     headers: {"Access-Control-Allow-Origin": "*"}
    // //    }).then(res => {
    // //     console.log(res["data"])
    // //    })
    // }, [count])
    return (
        <div className='stock-card'>
          <button onClick={fetchForcastHist}>FetchData</button>
          {loading && <h2>Loading</h2>}
          {stock?
           stock.map(data => {
                return(
                    <StockStats date={data["date"]} forecast={data["forecast"]}></StockStats>
                )
            })
          : <div>No data</div>}
        </div>
    )
}

export default StockCard;