import React, { useRef, useEffect } from "react";
import * as d3 from "d3";
import ChartUtils from "../utils/ChartUtils"

const DoubleHorizontalBarChart = (props: any) => { //= (data:[any,any][]) => { 
  const labels : any[] = props.labels;/* test data: [
    "acc_dist_index",
    "chaikin_money_flow",
    "ease_of_move",
    "williams_r",
    "rel_strength"
];*/
  const titles : any[] = ["Pearson Coefficient", "Importance Values"]
  const data : number[][] = props.data; /*[
    [0, 0.5, 0.1],
    [1,0.4, 0.2],
    [2,0.3, 0.3],
    [3,0.2, 0.4],
    [4,0.1, 0.5]
] /* /* */
  
  const canvas = useRef(null);
  
  const margin = {top: 50, right: 0, bottom: 50, left: 175};
  const width =  300;
  const height = 250;
  
  var xScaleRight = d3.scaleLinear()
    .range([0,width/2])
    .domain([0,ChartUtils.undefinedHandler(d3.max(data.map(d => d[2])),0)]);

  var xScaleLeft = d3.scaleLinear()
    .range([0,width/2])
    .domain([0,ChartUtils.undefinedHandler(d3.max(data.map(d => d[1])),0)]);
  
  var yScale = d3.scaleBand()
    .range([0,height])
    .domain(labels);
  
  const drawChart = () => {
    const g = d3.select(canvas.current);
    g.selectAll("*").remove();


    for(var i=0; i< labels.length; i++) {
      g.append("text")
        .attr("x", -10)
        .attr("y", ChartUtils.undefinedHandler(yScale(labels[i]),0) + yScale.bandwidth()/1.9) 
        .attr("font-size", "16px")
        .attr("text-anchor","end")
        .text(labels[i]);
    }

    g.append("text")
      .attr("x", width/2 -10)
      .attr("y", -20)
      .attr("font-size", "16px")
      .attr("text-anchor","end")
      .text(titles[0]);

    g.append("text")
      .attr("x", width/2 +10)
      .attr("y", -20) 
      .attr("font-size", "16px")
      .attr("text-anchor","start")
      .text(titles[1]);

    g.selectAll('rect')
        .data(data)
        .enter()
            .append('rect')
            .attr("x", function(d:number[]) : number { return width/2 - xScaleLeft(d[1])})
            .attr("y", function(d:any) : number {return ChartUtils.undefinedHandler(yScale(labels[d[0]]),0)})
            .attr('width', function(d:number[]) : number {return xScaleLeft(d[1])})
            .attr('height', yScale.bandwidth()-2)
            .style("fill","steelblue");

    g.selectAll('rect2')
        .data(data)
        .enter()
            .append('rect')
            .attr("x", width/2 + 5)
            .attr("y", function(d:any) : number {return ChartUtils.undefinedHandler(yScale(labels[d[0]]),0)})
            .attr('width', function(d:number[]) : number {return xScaleRight(d[2])})
            .attr('height', yScale.bandwidth()-2)
            .style("fill","red");   

  }
    
  useEffect(() => {
    drawChart();
  });

  return (
    <svg width={width+margin.left+margin.right} height={height+margin.top+margin.bottom}>
        <g
            ref={canvas}
            transform={`translate(${margin.left},${margin.top})`}
        />
    </svg>
  );

}

export default DoubleHorizontalBarChart;
