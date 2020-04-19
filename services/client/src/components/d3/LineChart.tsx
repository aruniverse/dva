import React, { useRef, useEffect } from "react";
import * as d3 from "d3";
import { ChartUtils } from "../utils/ChartUtils";

const colors = ["#66a61e", "#1b9e77", "#d95f02", "#7570b3", "#e7298a"];

const LineChart = (props: any) => {
  const data: number[][] = props.data;
  const dates = props.dates;
  const trades = props.trades;
  const title = props.title;
  const labels: string[] = props.labels;
  const canvas = useRef(null);

  const margin = { top: 50, right: 100, bottom: 50, left: 100 };
  const width = 500;
  const height = 500;
  var maxY = data[0][0];
  for (var i = 0; i < data.length; i++) {
    const tempValue = ChartUtils.undefinedHandler(d3.max(data[i]), 0);
    if (tempValue > maxY) {
      maxY = tempValue;
    }
  }

  const xScale = d3
    .scaleTime()
    .range([0, width])
    .domain([
      ChartUtils.undefinedHandler(d3.min(dates), 0),
      ChartUtils.undefinedHandler(d3.max(dates), 0),
    ]);
  const yScale = d3.scaleLinear().range([height, 0]).domain([0, maxY]);

  const addChartLine = (
    dataset: [any, number][],
    svg: d3.Selection<null, unknown, null, undefined>,
    color: string
  ) => {
    var line2 = d3
      .line()
      .x(function (d) {
        return xScale(d[0]);
      })
      .y(function (d) {
        return yScale(d[1]);
      })
      .curve(d3.curveMonotoneX);

    svg
      .append("path")
      .datum(dataset)
      .style("stroke", color)
      .attr("stroke-width", 1.5)
      .style("fill", "none")
      .attr("d", line2);
  };

  function addChartSymbol(
    svg: d3.Selection<null, unknown, null, undefined>,
    dataset: [any, number][],
    symbolClass: string,
    hasNoFill: boolean,
    color: string
  ) {
    svg
      .selectAll(symbolClass)
      .data(dataset)
      .enter()
      .append("circle")
      .attr("r", 5)
      .attr("cx", function (d) {
        return xScale(d[0]);
      })
      .attr("cy", function (d) {
        return yScale(d[1]);
      })
      .style("fill", color);

    if (hasNoFill) {
      svg
        .selectAll(symbolClass + "2")
        .data(dataset)
        .enter()
        .append("circle")
        .attr("r", 3)
        .attr("cx", (d) => xScale(d[0]))
        .attr("cy", (d) => yScale(d[1]))
        .style("fill", "white");
    }
  }

  const drawLineChart = () => {
    const g = d3.select(canvas.current);
    g.selectAll("*").remove();

    ChartUtils.initChart(
      g,
      title,
      "Time",
      "Portfolio Value ($)",
      xScale,
      yScale,
      width,
      height,
      0,
      height,
      margin.top,
      margin.left
    );
    for (var i = 0; i < data[0].length; i++) {
      var dataset: [any, number][] = [];
      for (var j = 0; j < dates.length; j++) {
        dataset.push([dates[j], data[j][i]]);
      }
      addChartLine(dataset, g, colors[i % colors.length]);
    }

    var enterLong: [any, number][] = [];
    var exitLong: [any, number][] = [];
    var enterShort: [any, number][] = [];
    var exitShort: [any, number][] = [];

    //1 = enter //2 = short
    for (i = 0; i < trades.length; i++) {
      for (j = 0; j < dates.length; j++) {
        if (trades[i][j] === 0) {
          exitLong.push([dates[j], data[j][i]]);
        } else if (trades[i][j] === 1) {
          enterLong.push([dates[j], data[j][i]]);
        } else if (trades[i][j] === 2) {
          exitShort.push([dates[j], data[j][i]]);
        } else if (trades[i][j] === 3) {
          enterShort.push([dates[j], data[j][i]]);
        }
      }
    }

    addChartSymbol(g, enterLong, "enterLong", false, "green");
    addChartSymbol(g, exitLong, "enterLong", true, "green");
    addChartSymbol(g, enterShort, "enterLong", false, "red");
    addChartSymbol(g, exitShort, "enterLong", true, "red");

    var legendData = [];
    for (i = 0; i < labels.length; i++) {
      legendData.push({
        color: colors[i % colors.length],
        name: labels[i],
        isLine: true,
      });
    }
    legendData.push({ color: "red", name: "Enter Short", hollow: false });
    legendData.push({ color: "red", name: "Exit Short", hollow: true });
    legendData.push({ color: "green", name: "Enter Long" });
    legendData.push({ color: "green", name: "Exit Long", hollow: true });

    ChartUtils.createLegend(g, legendData, width, height);
  };

  useEffect(() => {
    drawLineChart();
  });

  //https://medium.com/stationfive/how-to-create-a-pie-chart-with-d3-js-and-react-hooks-part-1-81bcd7f39b32
  return (
    //<div ref={canvas}></div>
    <svg
      width={width + margin.left + margin.right}
      height={height + margin.top + margin.bottom}
    >
      <g ref={canvas} transform={`translate(${margin.left},${margin.top})`} />
    </svg>
  );
};

export default LineChart;
