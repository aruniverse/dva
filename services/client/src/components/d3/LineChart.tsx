import React, { useRef, useEffect } from "react";
import * as d3 from "d3";
import ChartUtils from "../utils/ChartUtils"

const colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e"];

const LineChart = (data:[any,any][]) => {
  const canvas = useRef<HTMLDivElement>(null);
  //const data: [number,number][] = [[0,8], [1,5], [2,13], [3,9], [4,12]];
  //const canvas = useRef<HTMLDivElement>(null);

  const margin = {top: 50, right: 100, bottom: 50, left: 100};
  const width =  500;
  const height = 500;
  const transform = "translate("+margin['left'] +"," +margin.top +")";

  const xScale = d3.scaleTime().range([0,width]).domain([d3.min(data.map(d => d[0])),d3.max(data.map(d => d[0]))]);
  const yScale = d3.scaleLinear().range([height,0]).domain([0,d3.max(data.map(d => d[1]))]);
  
  const addChartLine = (dataset: [any,any][],svg: d3.Selection<SVGGElement,unknown,null,undefined>,xScale:any,yScale:any,color:string) => {
    var line2 = d3.line()
        .x(function(d) { return xScale(d[0]); })
        .y(function(d) { return yScale(d[1]); })
        .curve(d3.curveMonotoneX);

    svg.append("path")
      .datum(dataset)
      .style("stroke",color)
      .style("fill","none")
      .attr("d", line2);
  }

  const drawLineChart = (data: [any,any][],title : string,xScale : any, yScale: any) => {
    
    var svg = d3.select(canvas.current)
                .append("svg")
                  .attr("height",height + margin.top + margin.bottom)
                  .attr("width",width + margin.left + margin.right);

    var g = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    ChartUtils.initChart(g, title,"Year","Price ($)", xScale, yScale, width, height, margin.top, margin.left);
    addChartLine(data,g,xScale,yScale,"#d95f02");

    //var legendData=[{color:"#1b9e77",name:"actual"},{color:"#d95f02",name:"predicted"}]; //,{color:"#7570b3",name:"Midwest"},{color:"#e7298a",name:"Northeast"}]
    //createLegend(svg,legendData);

    /*legendData.forEach(cat => {
        var tempData = data.map(function(pt) {
                return {
                    date:pt.date, 
                    value:pt[cat.name]
                }
            }
        );
        addChartLine(tempData,svg,xScale,yScale,cat.color);
        //addChartSymbol(svg, tempData, xScale,yScale,cat.color,barChartPartial);
    */
  };

  useEffect(() => {
    drawLineChart(data, "HELP", xScale, yScale);
  });

  return (
    <div ref={canvas}></div>
  );

}

export default LineChart;