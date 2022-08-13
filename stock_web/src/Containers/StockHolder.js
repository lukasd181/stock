import StockCard from "../Components/StockCard";

const StockHolder = () => {
    return (
        <div className="stock-holder">
            <StockCard symbol={"AAPL"}></StockCard>
            <StockCard symbol={"NFLX"}></StockCard>
            <StockCard symbol={"AMZN"}></StockCard>
            <StockCard symbol={"GOOGL"}></StockCard>
        </div>
    )
}

export default StockHolder;