import { extractImgUrl } from "./utils/extractImgUrl";

const StockGraph = (props) => {
    const imgRelativePath = props.source.slice(18)
    const imgURL = extractImgUrl(imgRelativePath)

    return (
        <div>
            <img src={imgURL} width="450" height="170" alt="plot"></img>
        </div>
    )
}

export default StockGraph;