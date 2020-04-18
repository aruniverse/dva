import React, { useEffect, useState } from "react";
import withMainContainer from "../main/MainContainer";
import axios from "axios";
import { StockSymbol } from "../../types";
import { Button, CircularProgress, Grid, Input } from "@material-ui/core";
import {
  KeyboardDatePicker,
  MuiPickersUtilsProvider,
} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";

const Test = () => {
  const [loading, setLoading] = useState(false);
  const [ticker, setTicker] = useState("");
  const [endDate, setEndDate] = useState<Date | null>(new Date()); // today
  const tempDate = new Date();
  tempDate?.setMonth(tempDate.getMonth() - 3);
  const [startDate, setStartDate] = useState<Date | null>(tempDate); // 3 months ago

  const [data, setData] = useState<StockSymbol>();

  // useEffect(() => {
  //   getData();
  // }, []);

  const getData = async () => {
    setLoading(true);
    const response = await axios.get("/api/symbol", {
      params: {
        ticker: ticker,
        start_date: startDate?.toISOString(),
        end_date: endDate?.toISOString(),
      },
    });
    const { status, statusText, data } = response;
    console.log(response);
    if (status == 200) {
      setData(data);
      setLoading(false);
    } else {
      console.log(status, statusText);
      throw new Error(statusText);
    }
  };

  return (
    <div>
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
          >
            Default
          </Button>
        </Grid>
      </MuiPickersUtilsProvider>
      {loading ? (
        <CircularProgress style={{ alignContent: "center", height: "40px" }} />
      ) : (
        <>
          <h1 style={{ textAlign: "center" }}>{data?.symbol[0]}</h1>
          {data?.high.map((val, i) => {
            return (
              <h2 key={i} style={{ textAlign: "center" }}>
                {val}
              </h2>
            );
          })}
        </>
      )}
    </div>
  );
};

export default withMainContainer(Test);
