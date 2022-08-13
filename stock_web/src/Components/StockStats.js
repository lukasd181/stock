const StockStats = (props) => {
    return(
        <div className="stock-stats">
            <div className="stock-stats-text">{props.date} : {props.forecast}</div>
        </div>
    )
}

export default StockStats;