import React, { useEffect, useState } from "react";
import withMainContainer from "../main/MainStyle";
import axios from "axios";
import { StockSymbol } from "../../types/Symbol";

const Test = () => {
  const [data, setData] = useState<StockSymbol>();

  useEffect(() => {
    getData();
  }, []);

  const getData = async () => {
    const response = await axios.get("/symbol");
    const { status, statusText, data } = response;
    console.log(response);
    if (status == 200) {
      setData(data);
    } else {
      console.log(status, statusText);
      throw new Error(statusText);
    }
  };

  return (
    <div>
      <h1>{data?.symbol[0]}</h1>
      {data?.high.map((val, i) => {
        return (
          <h2 key={i} style={{ textAlign: "center" }}>
            {val}
          </h2>
        );
      })}
    </div>
  );
};

export default withMainContainer(Test);
