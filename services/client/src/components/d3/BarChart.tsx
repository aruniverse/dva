import React, { useRef, useState, useEffect } from "react";
import withMainContainer from "../main/MainContainer";
import * as d3 from "d3";

const BarChart = () => {
  const data: number[] = [8, 5, 13, 9, 12];
  const canvas = useRef<HTMLDivElement>(null);

  useEffect(() => drawBarChart(data), []);

  const drawBarChart = (data: number[]) => {
    d3.select(canvas.current)
      .selectAll("h2")
      .data(data)
      .enter()
      .append("h2")
      .text("New Temperature");
  };

  return <div ref={canvas}></div>;
};

export default withMainContainer(BarChart);
