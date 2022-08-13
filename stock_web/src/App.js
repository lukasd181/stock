import logo from './logo.svg';
import './App.css';
import StockCard from './Components/StockCard';
import StockHolder from './Containers/StockHolder';
import StockContainer from './Containers/StockContainer';

const shortNameArr = ["AAPL", "AMZN", "GOOGL", "NFLX", "META"]

function App() {
  return (
    <div className="App">

      {shortNameArr.map((shortName, index) => {
        return (
          <div key={index} className='container'>
            <StockContainer symbol={shortName} />
          </div>
        )
      })}
    </div>

  );
}

export default App;
