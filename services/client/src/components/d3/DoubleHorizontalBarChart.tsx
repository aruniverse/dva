import React, { useRef, useEffect } from "react";
import * as d3 from "d3";
import ChartUtils from "../utils/ChartUtils"

const DoubleHorizontalBarChart = () => { //= (data:[any,any][]) => { 
  const labels = [
    "acc_dist_index",
    "chaikin_money_flow",
    "ease_of_move",
    "williams_r",
    "rel_strength"
];
  const data = [
    [0, 0.2756677984891013, 0.3436117729993407],
    [1,0.2598309394640662, 0.23874349321875563],
    [2,0.14083624520208146, 0.056315968529372894],
    [3,0.10387139260015495, 0.14448808890026107],
    [4,0.21979362424459606, 0.21684067635226967]
]

for(var i=0; i<data.length; i++) {

}
  const title = "HELP";
  
  const canvas = useRef<HTMLDivElement>(null);
  
  const margin = {top: 50, right: 100, bottom: 50, left: 100};
  const width =  250;
  const height = 250;
  
  const undefinedHandler = (valToCheck: any, errVal : number) : number => {
    if(valToCheck) 
      return valToCheck;
    return errVal;
  }

  var xScaleRight = d3.scaleLinear()
    .range([width/2,width])
    .domain([0,undefinedHandler(d3.max(data.map(d => d[2])),0)]);

  var xScaleLeft = d3.scaleLinear()
    .range([0,width/2])
    .domain([0,undefinedHandler(d3.max(data.map(d => d[1])),0)]);
    //.domain([0,d3.max(data.map(d => d[0]))]);
  
  var yScale = d3.scaleBand()
    .range([height,0])
    .domain(labels);
  
  const drawChart = () => {
    var svg = d3.select(canvas.current)
    .append("svg")
      .attr("height",height + margin.top + margin.bottom)
      .attr("width",width + margin.left + margin.right);

    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    g.selectAll('rect')
        .data(data)
        .enter()
            .append('rect')
            .attr("x", function(d:number[]) : number { return width/2 - xScaleLeft(d[1])})
            .attr("y", function(d:any) : number {return undefinedHandler(yScale(labels[d[0]]),0)})
            .attr('width', function(d:number[]) : number {return xScaleLeft(d[1])})
            .attr('height', yScale.bandwidth()-2)
            .style("fill","steelblue");

    console.log(yScale("acc_dist_index"));

    g.selectAll('rect2')
        .data(data)
        .enter()
            .append('rect')
            .attr("x", width/2 + 5)
            .attr("y", function(d:any) : number {return undefinedHandler(yScale(labels[d[0]]),0)})
            .attr('width', function(d:number[]) : number {return xScaleRight(d[2])})
            .attr('height', yScale.bandwidth()-2)
            .style("fill","red");   

  }
    
  useEffect(() => {
    drawChart();
  });

  return (
    <div ref={canvas}></div>
  );

}

export default DoubleHorizontalBarChart;
