import React, { useRef, useEffect } from "react";
import * as d3 from "d3";
import { ChartUtils } from "../utils/ChartUtils";

const ScatterChart = (props: any) => {
  const data: number[][] = props.data;
  const label: string = props.label;
  const canvas = useRef(null);
  const margin = { top: 50, right: 100, bottom: 50, left: 100 };
  const width = 500;
  const height = 500;

  var maxX = data[0][0];
  var minX = data[0][0];
  var maxY = data[0][1];
  var minY = data[0][1];
  for (var i = 1; i < data.length; i++) {
    if (data[i][0] > maxX) {
      maxX = data[i][0];
    }
    if (data[i][0] < minX) {
      minX = data[i][0];
    }
    if (data[i][1] > maxY) {
      maxY = data[i][1];
    }
    if (data[i][1] < minY) {
      minY = data[i][1];
    }
  }

  const xScale = d3.scaleLinear().range([0, width]).domain([minX, maxX]);
  const yScale = d3.scaleLinear().range([height, 0]).domain([minY, maxY]);

  function addXYScatter(
    svg: d3.Selection<null, unknown, null, undefined>,
    xScale: any,
    yScale: any,
    color: string,
    radius: number
  ) {
    svg
      .selectAll("circle")
      .data(data)
      .enter()
      .append("circle")
      .attr("cx", function (d: number[]) {
        return xScale(d[0]);
      })
      .attr("cy", function (d: number[]) {
        return yScale(d[1]);
      })
      .attr("r", radius)
      .style("fill", color);
  }

  const drawScatterChart = (title: string, xScale: any, yScale: any) => {
    const g = d3.select(canvas.current);
    g.selectAll("*").remove();

    const possibleY = ChartUtils.undefinedHandler(
      d3.max([0, 1 - maxY / (maxY - minY)]),
      0
    );
    const yAxisShift = ChartUtils.undefinedHandler(d3.min([1, possibleY]), 1);

    ChartUtils.initChart(
      g,
      label,
      "% gain",
      "value",
      xScale,
      yScale,
      width,
      height,
      (1 - ChartUtils.undefinedHandler(d3.min([1,maxX / (maxX - minX)]),0)) * width,
      yAxisShift * height,
      margin.top,
      margin.left
    );
    addXYScatter(g, xScale, yScale, "#d95f02", 5);
  };

  useEffect(() => {
    drawScatterChart(label, xScale, yScale);
  });

  //https://medium.com/stationfive/how-to-create-a-pie-chart-with-d3-js-and-react-hooks-part-1-81bcd7f39b32
  return (
    <svg
      width={width + margin.left + margin.right}
      height={height + margin.top + margin.bottom}
    >
      <g ref={canvas} transform={`translate(${margin.left},${margin.top})`} />
    </svg>
  );
};

export default ScatterChart;
