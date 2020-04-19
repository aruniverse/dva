import ScatterChart from "./ScatterChart";
import LineChart from "./LineChart";
import React, { useState, useEffect } from "react";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Select from "@material-ui/core/Select";
import Slider from "@material-ui/core/Slider";
import Typography from "@material-ui/core/Typography";
import DoubleHorizontalBarChart from "./DoubleHorizontalBarChart";
import SliderCard from "../ui/SliderCard";
import withMainContainer from "../main/MainContainer";
import { StockAnalysis } from "../../types";
//import CurrentPosition from "../../utils/CurrentPosition";
import axios from "axios";
import { sample_data } from "../../data/sample";

export enum CurrentPosition {
  Short = 1,
  Neutral = 2,
  Long = 3,
}

export enum LastPositionChange {
  NoChange = -1,
  ExitLong = 0,
  EnterLong = 1,
  ExitShort = 2,
  EnterShort = 3,
}

const LoadChart = () => {
  const [data, setData] = useState<StockAnalysis>(sample_data);
  var final: JSX.Element[] = [];
  const [predictionTerm, updateTerm] = useState(5);
  const [longEnter, setLongEnter] = useState(4);
  const [longExit, setLongExit] = useState(3);
  const [shortEnter, setShortEnter] = useState(1);
  const [shortExit, setShortExit] = useState(2);
  const [rsiFlip, setrsiFlip] = useState(50);

  const getData = async () => {
    const response = await axios.get("/api/symbol/example");
    const { status, statusText } = response;
    console.log(response);
    if (status == 200) {
      console.log(response.data);
      setData(response.data);
      console.log("set data");
    } else {
      console.log(status, statusText);
      throw new Error(statusText);
    }
  };

  // useEffect(() => {
  //   getData();
  // }, []);

  const handleEnterLong = (event: any, value: number | number[]) => {
    if (typeof value == "number") {
      setLongEnter(value);
    }
  };

  const handleExitLong = (event: any, value: number | number[]) => {
    if (typeof value == "number") {
      setLongExit(value);
    }
  };

  const handleEnterShort = (event: any, value: number | number[]) => {
    if (typeof value == "number") {
      setShortEnter(value);
    }
  };

  const handleExitShort = (event: any, value: number | number[]) => {
    if (typeof value == "number") {
      setShortExit(value);
    }
  };

  const handleRSIShort = (event: any, value: number | number[]) => {
    if (typeof value == "number") {
      setrsiFlip(value);
    }
  };

  const addGridOfX = (val: number) => {
    final.push(<Grid item lg={2}></Grid>);
  };

  const handleChange = (event: any, value: number | number[]) => {
    if (typeof value == "number") {
      updateTerm(value);
    }
  };

  addGridOfX(2);
  final.push(
    SliderCard(
      handleEnterLong,
      "Enter Long",
      "Select cutoff percentage where strategy enters long position",
      0,
      5,
      4,
      data.move
    )
  );
  final.push(
    SliderCard(
      handleExitLong,
      "Exit Long",
      "Select cutoff percentage where strategy exits long position",
      0,
      5,
      3,
      data.move
    )
  );
  final.push(
    SliderCard(
      handleEnterShort,
      "Enter Short",
      "Select cutoff percentage where strategy enters short position",
      0,
      5,
      2,
      data.move
    )
  );
  final.push(
    SliderCard(
      handleExitShort,
      "Exit Short",
      "Select cutoff percentage where strategy exit short position",
      0,
      5,
      3,
      data.move
    )
  );
  addGridOfX(2);
  addGridOfX(5);
  final.push(
    SliderCard(
      handleRSIShort,
      "RSI",
      "Select RSI value to go long/short",
      1,
      99,
      50,
      []
    )
  );
  addGridOfX(2);
  addGridOfX(2);
  final.push(
    SliderCard(
      handleChange,
      "Enter prediction term",
      "Select term to compare gain vs indicator",
      1,
      60,
      1,
      []
    )
  );
  addGridOfX(2);
  addGridOfX(2);

  /******************* double bar chart *****************************/
  var term: any = "term_5";
  var doubleData = [];
  var key = "fasdklj";
  for (var i = 0; i < 5; i++) {
    doubleData.push([
      i,
      data.predict.term_5.importance_values[i],
      data.f_regression.term_5.p_values[i],
    ]);
  }

  final.push(
    <Grid item lg={4} key={key}>
      <Card variant="outlined">
        <DoubleHorizontalBarChart
          labels={data.f_regression["indicator_list"]}
          data={doubleData}
        ></DoubleHorizontalBarChart>
      </Card>
    </Grid>
  );

  /* ************ line chart ***************************/
  var keyPlot = 1098;
  const startPrice = 10000;
  var j = 0;
  var dates: Date[] = [];
  var returnData: number[][] = [];
  var strategyLabels = [];

  for (var i = 0; i < data["dates"].length; i++) {
    dates.push(new Date(data["dates"][i]));
    returnData[i] = [];
  }

  var j = 0;
  var trades: number[][] = [];
  var k = 0;

  const getType = (vals: string[]): number => {
    var val = 0;
    if (vals[1] == "enter") {
      val += 1;
    }
    if (vals[2] == "short") {
      val += 2;
    }
    return val;
  };

  Object.entries(data["strategy"]).forEach(([key, value]) => {
    for (var i = 0; i < value["cum_return"].length; i++) {
      returnData[i][j] = startPrice * (1 + value["cum_return"][i]);
    }
    trades[j] = data.dates.map((d) =>
      d === value["actions"][k][0] ? getType(value["actions"][k++]) : -1
    );
    strategyLabels.push(key);
    j++;
  });

  var currentTrade = CurrentPosition.Neutral;
  var currentPortfolioValue = 10000;
  var tempChanges: number[] = [];

  for (i = 0; i < data.indicators["rel_strength"].length; i++) {
    var predict_move_rsi = data["indicators"]["rel_strength"][i];
    changedPostion = LastPositionChange.NoChange;
    //check long position
    if (predict_move_rsi >= rsiFlip) {
      if (currentTrade == CurrentPosition.Short) {
        changedPostion = LastPositionChange.EnterLong;
      }
      currentTrade = CurrentPosition.Long;
      currentPortfolioValue *= 1 + data["daily_ret"][i];
    } else {
      if (currentTrade == CurrentPosition.Long) {
        changedPostion = LastPositionChange.EnterShort;
      }
      currentTrade = CurrentPosition.Short;
      currentPortfolioValue *= 1 - data["daily_ret"][i];
    }

    returnData[i][j] = currentPortfolioValue;
    tempChanges.push(changedPostion);
  }

  trades.push(tempChanges);
  strategyLabels.push("RSI at " + rsiFlip);
  j++;

  var currentTrade = CurrentPosition.Neutral;
  var changedPostion = LastPositionChange.NoChange;
  currentPortfolioValue = 10000;
  tempChanges = [];

  for (i = 0; i < data.predict.term_60.predict.length; i++) {
    var predictedMove = data.predict.term_60.predict[i];
    changedPostion = LastPositionChange.NoChange;

    //check long position
    if (currentTrade == CurrentPosition.Long) {
      if (predictedMove <= longExit) {
        if (predictedMove < shortEnter) {
          currentTrade = CurrentPosition.Short;
          changedPostion = LastPositionChange.EnterShort;
        } else {
          currentTrade = CurrentPosition.Neutral;
          changedPostion = LastPositionChange.ExitLong;
        }
      }
    } else if (currentTrade == CurrentPosition.Neutral) {
      if (predictedMove >= longEnter) {
        currentTrade = CurrentPosition.Long;
        changedPostion = LastPositionChange.EnterLong;
      } else if (predictedMove <= shortEnter) {
        currentTrade = CurrentPosition.Short;
        changedPostion = LastPositionChange.EnterShort;
      }
    } else {
      // currently shortign
      if (predictedMove > shortExit) {
        if (predictedMove > longEnter) {
          currentTrade = CurrentPosition.Long;
          changedPostion = LastPositionChange.EnterLong;
        } else {
          currentTrade = CurrentPosition.Neutral;
          changedPostion = LastPositionChange.ExitShort;
        }
      }
    }

    if (currentTrade == CurrentPosition.Long) {
      currentPortfolioValue *= 1 + data["daily_ret"][i];
    } else if (currentTrade == CurrentPosition.Short) {
      currentPortfolioValue *= 1 - data["daily_ret"][i];
    }
    returnData[i][j] = currentPortfolioValue;
    tempChanges.push(changedPostion);
  }
  trades.push(tempChanges);
  strategyLabels.push("Random Forest");

  final.push(
    <Grid item lg={4} key={keyPlot}>
      <Card variant="outlined">
        <LineChart
          data={returnData}
          dates={dates}
          trades={trades}
          labels={strategyLabels}
          title="Return"
        ></LineChart>
      </Card>
    </Grid>
  );

  /*** Scatter Plots ****************** */
  keyPlot++;

  addGridOfX(5);
  addGridOfX(5);
  addGridOfX(5);
  addGridOfX(5);
  addGridOfX(5);

  Object.entries(data["indicators"]).forEach(([key, value]) => {
    var scatterData: number[][] = [];
    for (var i = 0; i < data["dates"].length - predictionTerm; i++) {
      scatterData[i] = [];
      scatterData[i].push(
        data["cum_return"][i + predictionTerm] - data["cum_return"][i]
      );
      scatterData[i].push(value[i]);
    }
    final.push(
      <Grid item lg={4} key={key}>
        <Card variant="outlined">
          <ScatterChart data={scatterData} label={key}></ScatterChart>
        </Card>
      </Grid>
    );
    keyPlot++;
  });

  console.log("runs");

  return (
    <div>
      <Grid container spacing={1}>
        {final}
      </Grid>
    </div>
  );
};

export default withMainContainer(LoadChart);
// export default LoadChart;
