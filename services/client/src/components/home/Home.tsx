import React from "react";
import withMainContainer from "../main/MainContainer";
import { ReactComponent as StockMarket } from "../../images/stock_color.svg";
import Stocks from "../../images/stocks.jpg";

const Home = () => {
  return (
    <div className="Home">
      <img
        src={Stocks}
        className="StocksImage"
        style={{ height: 720, width: 1280 }}
      />
      <h1>Team 128: TBD</h1>
      <p>
        The goal of this visualization tool is to evaluate the effectiveness of
        indicators that can be implemented in machine learning models for
        predicting stock market prices. Key features of this tool includes:
        <li>
          The ability to visually and interactively determine the effectiveness
          of market indicators based on historical data.
        </li>
        <li>
          The flexibility to investigate the performance of indicators under
          different market conditions.
        </li>
        <li>
          Present a comparison of the performance of algorithms implementing the
          selected indicator
        </li>
      </p>
    </div>
  );
};

export default withMainContainer(Home);
