import React, { useRef, useEffect } from "react";
import * as d3 from "d3";
import ChartUtils from "../utils/ChartUtils"

const colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e"];

const LineChart = (props: any) => {
  const data : number[][] = props.data;
  const dates = props.dates;
  const title = props.title;
  const canvas = useRef<HTMLDivElement>(null);
  //const data: [number,number][] = [[0,8], [1,5], [2,13], [3,9], [4,12]];
  //const canvas = useRef<HTMLDivElement>(null);

  const margin = {top: 50, right: 100, bottom: 50, left: 100};
  const width =  500;
  const height = 500;
  var maxY = data[0][0];
  for(var i=0; i<data.length;i++) {
    const tempValue = ChartUtils.undefinedHandler(d3.max(data[i]),0);
    if(tempValue > maxY) {
      maxY = tempValue;
    }
  }

  const xScale = d3.scaleTime().range([0,width]).domain([ChartUtils.undefinedHandler(d3.min(dates),0),ChartUtils.undefinedHandler(d3.max(dates),0)]);
  const yScale = d3.scaleLinear().range([height,0]).domain([0,maxY]);
  
  const addChartLine = (dataset: [any,number][],svg: d3.Selection<SVGGElement,unknown,null,undefined>,color:string) => {
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

  const drawLineChart = () => {
    
    var svg = d3.select(canvas.current)
                .append("svg")
                  .attr("height",height + margin.top + margin.bottom)
                  .attr("width",width + margin.left + margin.right);

    var g = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    ChartUtils.initChart(g, title,"Year","Price ($)", xScale, yScale, width, height, 0, height, margin.top, margin.left);
    for(var i=0; i<data[0].length; i++) {
      var dataset : [any,number][] = [];
      for(var j=0; j<dates.length; j++) {
        dataset.push([dates[j] ,data[j][i]]);
      }
      addChartLine(dataset,g,colors[i%colors.length]);
    }

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
    drawLineChart();
  });

  return (
    <div ref={canvas}></div>
  );

}

export default LineChart;