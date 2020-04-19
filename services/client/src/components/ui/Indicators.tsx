import ScatterChart from "../d3/ScatterChart";
import React, { useState } from "react";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import DoubleHorizontalBarChart from "../d3/DoubleHorizontalBarChart";
import SliderCard from "../ui/SliderCard";
import FormLabel from "@material-ui/core/FormLabel";
import FormControl from "@material-ui/core/FormControl";
import FormGroup from "@material-ui/core/FormGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import { StockAnalysis } from "../../types";
import withMainContainer from "../main/MainContainer";

interface StringBoolean {
  [id: string]: boolean;
}

interface IndicatorsLayoutProps {
  data: StockAnalysis;
}

interface IndicatorTextMapInterface {
  [key: string]: {
    label: string;
    description: string;
    more: string;
  };
}

const IndicatorTextMap: IndicatorTextMapInterface = {
  acc_dist_index: {
    label: "Accumulation/Distribution Index",
    description: "An indicator intended to relate price and volume.",
    more: "https://en.wikipedia.org/wiki/Accumulation/distribution_index",
  },
  chaikin_money_flow: {
    label: "Chaikin Money flow",
    description:
      "Measures the amount of Money Flow Volume over a specific period.",
    more:
      "http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_money_flow_cmf",
  },
  ease_of_move: {
    label: "Ease of Movement",
    description:
      "Relates an asset's price change to its volume and is particularly useful for assessing the strength of a trend.",
    more: "https://en.wikipedia.org/wiki/Ease_of_movement",
  },
  williams_r: {
    label: "Williams R",
    description:
      "Reflects the level of the close relative to the highest high for the look-back period. ",
    more:
      "https://school.stockcharts.com/doku.php?id=technical_indicators:williams_r",
  },
  rel_strength: {
    label: "Relative Strength Index",
    description:
      "Compares the magnitude of recent gains and losses over a specified time period to measure speed and change of price movements of a security.",
    more: "https://www.investopedia.com/terms/r/rsi.asp",
  },
};

export const IndicatorsLayout = ({ data }: IndicatorsLayoutProps) => {
  var final: JSX.Element[] = [];
  var doubleData = [];
  var key = "fasdklj";
  var keyPlot = 1098;
  var termType: string = "term_5";
  const p_values: string = "p_values";

  var labelStrings: string[] = data.indicator_list;
  var labels: StringBoolean = {};

  Object.entries(data.indicators).forEach(([key]) => {
    labels[key] = true;
  });

  const [predictionTerm, updateTerm] = useState(5);

  const [state, setState] = useState<StringBoolean>(labels);
  const handleChange = (event: any, value: number | number[]) => {
    if (typeof value == "number") {
      updateTerm(value);
    }
  };

  const handleCheckBoxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({ ...state, [event.target.value]: event.target.checked });
  };

  const addGridOfX = (val: number) => {
    final.push(<Grid item lg={2}></Grid>);
  };

  addGridOfX(5);

  /******************* double bar chart *****************************/
  for (var i = 0; i < data.f_regression[termType][p_values].length; i++) {
    doubleData.push([
      i,
      data.predict[termType]["importance_values"][i],
      data.f_regression[termType][p_values][i],
    ]);
  }

  final.push(
    <Grid item lg={4} key={key}>
      <Card variant="outlined">
        <DoubleHorizontalBarChart
          labels={labelStrings.map((val) => IndicatorTextMap[val].label)}
          data={doubleData}
        ></DoubleHorizontalBarChart>
        <p style={{ textAlign: "center" }}>
          This plot shows indicators most likely to predict future stock
          direction
        </p>
      </Card>
    </Grid>
  );

  /*** slider + indicator card **********/

  const checkboxes = labelStrings.map(function (val: string) {
    return (
      <FormControlLabel
        control={
          <Checkbox
            checked={state[val]}
            onChange={handleCheckBoxChange}
            value={val}
          ></Checkbox>
        }
        label={IndicatorTextMap[val].label}
      ></FormControlLabel>
    );
  });

  final.push(
    <Grid item lg={2}>
      <Card variant="outlined">
        <FormControl component="fieldset">
          <FormLabel component="legend">Select Indicators</FormLabel>
          <FormGroup>{checkboxes}</FormGroup>
        </FormControl>
      </Card>
    </Grid>
  );

  final.push(
    SliderCard(
      handleChange,
      "Enter prediction term",
      "Select term to compare gain vs indicator",
      1,
      data.dates.length - 5,
      1,
      []
    )
  );

  /*** Scatter Plots ****************** */
  keyPlot++;

  Object.entries(data.indicators).forEach(([key, value]) => {
    //console.log(labels.get(key));
    if (state[key]) {
      var scatterData: any[][] = [];
      for (var i = 0; i < data.dates.length - predictionTerm; i++) {
        scatterData[i] = [];
        scatterData[i].push(
          data.cum_return[i + predictionTerm] - data.cum_return[i]
        );
        scatterData[i].push(value[i]);
      }
      final.push(
        <Grid item lg={4} key={key}>
          <Card variant="outlined">
            <ScatterChart
              data={scatterData}
              label={IndicatorTextMap[key].label}
            ></ScatterChart>
          </Card>
          <p style={{ textAlign: "center" }}>
            {IndicatorTextMap[key].description}
          </p>
          <div className="MoreInfo" style={{ textAlign: "right" }}>
            <a
              href={IndicatorTextMap[key].more}
              target="_blank"
              rel="noopener noreferrer"
            >
              {"For More Info"}
            </a>
          </div>
        </Grid>
      );
      keyPlot++;
    }
  });

  return (
    <div className="IndicatorLayout">
      <Grid container spacing={1}>
        {final}
      </Grid>
    </div>
  );
};

export default withMainContainer(IndicatorsLayout);
