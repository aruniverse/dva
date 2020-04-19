import React, { useState } from "react";
import { StockAnalysis } from "../../types";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import LineChart from "../d3/LineChart";
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import SliderCard from "../ui/SliderCard";
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';
import { SampleData2 } from "../../data/sample2";

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

  interface StringBoolean {
    [id:string]:boolean
  }

const StrategiesLayout = () => {

  var data = SampleData2;
  var keyPlot = 1098;
  const startPrice = 10000;
  var j = 0;
  var dates: Date[] = [];
  var returnData: number[][] = [];
  var strategyLabels = ["bollinger", "williams_r", "RSI", "Random Forest", "Buy and Hold"];
  var trades: number[][] = [];
  var k = 0;

  var final: JSX.Element[] = [];
  const [predictionTerm, updateTerm] = useState(5);
  const [longEnter, setLongEnter] = useState(4);
  const [longExit, setLongExit] = useState(3);
  const [shortEnter, setShortEnter] = useState(1);
  const [shortExit, setShortExit] = useState(2);
  const [rsiFlip, setrsiFlip] = useState(50);
  var strategyLabelsMap : StringBoolean = {};

    // 
  for(i=0; i<strategyLabels.length; i++) {
    strategyLabelsMap[strategyLabels[i]]=true;
  }

  const [state, setState] = useState<StringBoolean>(strategyLabelsMap);   
  const handleRSIShort = (event: any, value: number | number[]) => {
        if (typeof value == "number") {
        setrsiFlip(value);
        }
    };
  
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

  const handleChange = (event: any, value: number | number[])  => {
      if(typeof(value)=="number") {
          updateTerm(value);
      }
  };

    
  /* ************ line chart ***************************/

  for (var i = 0; i < data["dates"].length; i++) {
    dates.push(new Date(data["dates"][i]));
    returnData[i] = [];
  }

  //process strategies straight from strategies
  const getType = (vals: string[]): number => {
    var val = 0;
    if (vals[1] === "enter") {
      val += 1;
    }
    if (vals[2] === "short") {
      val += 2;
    }
    return val;
  };

  Object.entries(data["strategy"]).forEach(([key, value]) => {
    if(state[key]) {
      for (i = 0; i < value["cum_return"].length; i++) {
        returnData[i][j] = startPrice * (1 + value["cum_return"][i]);
      }
      k=0;
      for(i=0; i<data.dates.length; i++) {
          var date1 = new Date(data.dates[i]);
          var date2 = new Date(value["actions"][k][0]);
          if(date1 > date2) {
              k++;
          } else {
              break;
          }
      }
      trades[j] = data.dates.map((d) =>
        d === value["actions"][k][0] ? getType(value["actions"][k++]) : -1
      );
      j++;
    }
  });

  var currentTrade = CurrentPosition.Neutral;
  var changedPostion = LastPositionChange.NoChange;
  var currentPortfolioValue = 10000;
  var tempChanges: number[] = [];

  // Process data for RSI strategy
  if(state["RSI"]) {
    for (i = 0; i < data.indicators["rel_strength"].length; i++) {
      var predict_move_rsi = data["indicators"]["rel_strength"][i];
      changedPostion = LastPositionChange.NoChange;
      //check long position
      if (predict_move_rsi >= rsiFlip) {
        if (currentTrade === CurrentPosition.Short) {
          changedPostion = LastPositionChange.EnterLong;
        }
        currentTrade = CurrentPosition.Long;
        currentPortfolioValue *= 1 + data["daily_ret"][i];
      } else {
        if (currentTrade === CurrentPosition.Long) {
          changedPostion = LastPositionChange.EnterShort;
        }
        currentTrade = CurrentPosition.Short;
        currentPortfolioValue *= (1 - data["daily_ret"][i]);
      }

      returnData[i][j] = currentPortfolioValue;
      tempChanges.push(changedPostion);
    }

    trades.push(tempChanges);
    //strategyLabels.push("RSI at " + rsiFlip);
    j++;
  }

  // Process data for random forest strategy
  var priceExit = 0;
  currentTrade = CurrentPosition.Neutral;
  changedPostion = LastPositionChange.NoChange;
  currentPortfolioValue = 10000;
  tempChanges = [];

  if(state['Random Forest']) {
    for (i = 0; i < data.predict["term_"+predictionTerm].predict.length; i++) {
      var predictedMove = data.predict["term_"+predictionTerm].predict[i];
      changedPostion = LastPositionChange.NoChange;

      //check long position
      if (currentTrade === CurrentPosition.Long) {
        if (currentPortfolioValue >= priceExit) {
          if (predictedMove < shortEnter) {
            currentTrade = CurrentPosition.Short;
            changedPostion = LastPositionChange.EnterShort;
            priceExit = currentPortfolioValue*(1-shortExit/100);
          } else {
            currentTrade = CurrentPosition.Neutral;
            changedPostion = LastPositionChange.ExitLong;
          }
        }
      } else if (currentTrade === CurrentPosition.Neutral) {
        if (predictedMove >= longEnter) {
          currentTrade = CurrentPosition.Long;
          changedPostion = LastPositionChange.EnterLong;
          priceExit = currentPortfolioValue*(1+longExit/100);
        } else if (predictedMove <= shortEnter) {
          currentTrade = CurrentPosition.Short;
          changedPostion = LastPositionChange.EnterShort;
          priceExit = currentPortfolioValue*(1-shortExit/100);
        }
      } else {
        // currently shorting
        if (predictedMove > shortExit) {
          if (predictedMove > longEnter) {
            currentTrade = CurrentPosition.Long;
            changedPostion = LastPositionChange.EnterLong;
            priceExit = currentPortfolioValue*(1+longExit/100);

          } else {
            currentTrade = CurrentPosition.Neutral;
            changedPostion = LastPositionChange.ExitShort;
          }
        }
      }

      if (currentTrade === CurrentPosition.Long) {
        currentPortfolioValue *= 1 + data["daily_ret"][i];
      } else if (currentTrade === CurrentPosition.Short) {
        currentPortfolioValue *= 1 - data["daily_ret"][i];
      }
      returnData[i][j] = currentPortfolioValue;
      tempChanges.push(changedPostion);
    }
    trades.push(tempChanges);
    j++;
  }
  // add buy and hold strategy...
  if(state["Buy and Hold"]) {
    currentPortfolioValue = 10000;
    tempChanges = [];
    for(i=0; i<data.daily_ret.length; i++) {
      returnData[i][j] = currentPortfolioValue*(1+data.daily_ret[i]);
      tempChanges[i]=-1;
    }
    trades.push(tempChanges);
  }

  const handleCheckBoxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setState({ ...state, [event.target.name]: event.target.checked });
  };
  const checkboxes = strategyLabels.map(function(val:string) { return <FormControlLabel control={<Checkbox checked={state[val]} onChange={handleCheckBoxChange} name={val}></Checkbox>} label={val}></FormControlLabel>});

  final.push(
      <Grid item lg={2} key={"strategies"}>
          <Card variant="outlined">
              <CardContent>
                  <FormControl component="fieldset">
                      <FormLabel component="legend">Select Strategies to Show</FormLabel>
                      <FormGroup>
                          {checkboxes}
                      </FormGroup>
                  </FormControl>
              </CardContent>
          </Card>
      </Grid>
  );

  // push strategy filter before ...
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

  // strategy parameters

  var marks = [];
  for(i=0; i<data.move.length; i++) {
      marks.push({value:i+1,label:String(data.move[i]+"%")})
  }

  var marksTerms : any[] = [];
  for(i=0; i<data.term.length; i++) {
    marksTerms.push({value:data.term[i],label:String(data.term[i])})
  }   

  final.push(
    <Grid key={"randomForest"} item lg={2}>

    <Card variant="outlined">
        <Typography id="discrete-slider-small-steps" gutterBottom>
                    <b>{"Random Forest Parameters"}:</b>
        </Typography>
        <Card variant="outlined">
            <CardContent>
                <Typography id="discrete-slider-small-steps" gutterBottom>
                    <b>{"Enter Long"}:</b>
                </Typography>
                <p>
                    {"Select cutoff percentage where strategy enters long position"}
                </p>
                <Slider
                    name="enterLong"
                    defaultValue={3}
                    step={1}
                    marks={marks}
                    min={1}
                    max={6}
                    onChange={handleEnterLong}
                    valueLabelDisplay="auto"
                />
            </CardContent>
        </Card>
        <Card variant="outlined">
            <CardContent>
                <Typography id="discrete-slider-small-steps" gutterBottom>
                    <b>{"Exit Long"}:</b>
                </Typography>
                <p>
                    {"Select cutoff percentage where strategy exits long position"}
                </p>
                <Slider
                    name={"exitLong"}
                    defaultValue={0}
                    step={0.01}
                    marks={[]}
                    min={0}
                    max={5}
                    onChange={handleExitLong}
                    valueLabelDisplay="auto"
                />
            </CardContent>
        </Card>

        <Card variant="outlined">
            <CardContent>
                <Typography id="discrete-slider-small-steps" gutterBottom>
                    <b>{"Exit Short"}:</b>
                </Typography>
                <p>
                    {"Select cutoff percentage where strategy exits short position"}
                </p>
                <Slider
                    name={"exitShort"}
                    defaultValue={0}
                    step={0.01}
                    marks={[]}
                    min={-5}
                    max={0}
                    onChange={handleExitShort}
                    valueLabelDisplay="auto"
                />
            </CardContent>
        </Card>

        <Card variant="outlined">
            <CardContent>
                <Typography id="discrete-slider-small-steps" gutterBottom>
                    <b>{"Enter Short"}:</b>
                </Typography>
                <p>
                    {"Select cutoff percentage where strategy enters short position"}
                </p>
                <Slider
                    name={"enterShort"}
                    defaultValue={3}
                    marks={marks}
                    min={1}
                    max={6}
                    onChange={handleEnterShort}
                    valueLabelDisplay="auto"
                />
            </CardContent>
        </Card>

        <Card variant="outlined">
            <CardContent>
                <Typography id="discrete-slider-small-steps" gutterBottom>
                    <b>{"Enter prediction term"}:</b>
                </Typography>
                <p>
                    {"Select length of term that random forest trains on"}
                </p>
                <Slider
                    defaultValue={5}
                    step={null}
                    marks={marksTerms}
                    min={0}
                    max={40}
                    onChange={handleChange}
                    valueLabelDisplay="auto"
                />
            </CardContent>
        </Card>
    </Card>
    </Grid>
); 

  final.push(
    SliderCard(     handleRSIShort,"RSI",  "Select RSI value to go long/short",   1,   99,  50,  []
    )
  );

  return (
    <div><Grid container spacing={1}>{final}</Grid></div>
  );
}

export default StrategiesLayout;