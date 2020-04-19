import React, { useState } from "react";
import withMainContainer from "../main/MainContainer";
import { StockAnalysis } from "../../types";
import { CircularProgress, Grid, Button, Input } from "@material-ui/core";
import {
  MuiPickersUtilsProvider,
  KeyboardDatePicker,
} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import axios from "axios";
import StrategiesLayout from "./Strategies";
import { FormatDate } from "../utils/FormatDate";

// const API_ENDPOINT = "http://dvateam128.webfactional.com/api/analysis";
const API_ENDPOINT = "/api/analysis/example";

const StrategiesPage = () => {
  const [loading, setLoading] = useState(false);
  const [ticker, setTicker] = useState("");
  const [endDate, setEndDate] = useState<Date | null>(new Date()); // today
  const tempDate = new Date();
  tempDate?.setMonth(tempDate.getMonth() - 3);
  const [startDate, setStartDate] = useState<Date | null>(tempDate); // 3 months ago
  const [data, setData] = useState<StockAnalysis>();

  const httpClient = axios.create();
  httpClient.defaults.timeout = 20000;

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
    <div className="StrategiesPage">
      <h1>Strategies</h1>
      <p>
        This page is used to determine which strategies are useful in a model to
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
            style={{ justifySelf: "left" }}
            onClick={() => getData()}
            disabled={!ticker}
          >
            Run
          </Button>
        </Grid>
      </MuiPickersUtilsProvider>
      {loading ? (
        <CircularProgress style={{ alignContent: "center", height: "40px" }} />
      ) : (
        data && <StrategiesLayout data={data} />
      )}
    </div>
  );
};

export default withMainContainer(StrategiesPage);
