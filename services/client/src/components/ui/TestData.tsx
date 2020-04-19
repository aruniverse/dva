import React from "react";
import { StockAnalysis } from "../../types";
import IndicatorsLayout from "./Indicators";
import { SampleData2 } from "../../data/sample2";

const TestData = () => {
  return <IndicatorsLayout data={SampleData2} />;
};

export default TestData;
