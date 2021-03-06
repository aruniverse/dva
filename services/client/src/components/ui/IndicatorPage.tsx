import React, { useState } from "react";
import withMainContainer from "../main/MainContainer";
import { StockAnalysis } from "../../types";
import {
  CircularProgress,
  Grid,
  Button,
  Input,
  Backdrop,
} from "@material-ui/core";
import {
  MuiPickersUtilsProvider,
  KeyboardDatePicker,
} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import axios from "axios";
import { FormatDate } from "../utils/FormatDate";
import { IndicatorsLayout } from "./Indicators";

// const API_ENDPOINT = "http://dvateam128.webfactional.com/api/analysis";
// const API_ENDPOINT =
//   "http://dvateam128.webfactional.com/api/analysis/example";
// const API_ENDPOINT = "/api/analysis/example";
const API_ENDPOINT = "/api/analysis";

const IndicatorsPage = () => {
  const [loading, setLoading] = useState(false);
  const [ticker, setTicker] = useState("");
  const [endDate, setEndDate] = useState<Date | null>(new Date()); // today
  const tempDate = new Date();
  tempDate?.setMonth(tempDate.getMonth() - 6);
  const [startDate, setStartDate] = useState<Date | null>(tempDate); // 6 months ago
  const [data, setData] = useState<StockAnalysis>();

  const httpClient = axios.create();
  // httpClient.defaults.timeout = 20000;

  const getData = async () => {
    setLoading(true);
    const response = await httpClient.get(API_ENDPOINT, {
      params: {
        symbol: ticker,
        start_date: FormatDate(startDate),
        end_date: FormatDate(endDate),
      },
    });
    const { status, statusText, data } = response;
    console.log(response);
    if (status == 200) {
      setData(data);
      setLoading(false);
    } else {
      setLoading(false);
      console.log(status, statusText);
      throw new Error(statusText);
    }
  };

  return (
    <div className="IndicatorPage">
      <h1>Indicators</h1>
      <p>
        This page is used to determine which indicators are useful in a model to
        predict stock direction. Please enter the Stock Ticker, the Start Date,
        End Date and then run!
      </p>
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
        <Grid container justify="space-around">
          <Input
            placeholder="Enter Stock Ticker"
            inputProps={{ "aria-label": "description" }}
            onChange={(event: { target: { value: any } }) =>
              setTicker(event?.target.value)
            }
          />
          <KeyboardDatePicker
            margin="normal"
            id="date-picker-dialog"
            label="Start Date"
            format="MM/dd/yyyy"
            value={startDate}
            onChange={setStartDate}
            KeyboardButtonProps={{
              "aria-label": "change date",
            }}
          />
          <KeyboardDatePicker
            margin="normal"
            id="date-picker-dialog"
            label="End Date"
            format="MM/dd/yyyy"
            value={endDate}
            onChange={setEndDate}
            KeyboardButtonProps={{
              "aria-label": "change date",
            }}
          />
          <Button
            variant="contained"
            onClick={() => getData()}
            disabled={!ticker}
            color="primary"
          >
            Run
          </Button>
        </Grid>
      </MuiPickersUtilsProvider>
      <p style={{ textAlign: "center" }}>
        NOTE: The Start Date and End Date needs to be a minimum of 180 days
        apart. The farther apart the dates are, the better the results. Good
        Tickers to test with include "MSFT", "AAPL", "AMZN", "FB", "TSLA". Only
        stocks traded on NASDAQ are allowed.
      </p>
      {loading ? (
        <Backdrop open={loading}>
          <CircularProgress
            style={{ alignContent: "center", height: "40px" }}
          />
        </Backdrop>
      ) : (
        data && <IndicatorsLayout data={data} />
      )}
    </div>
  );
};

export default withMainContainer(IndicatorsPage);
