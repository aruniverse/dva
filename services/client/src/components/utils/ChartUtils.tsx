
import * as d3 from "d3";

export class ChartUtils {
 static initChart(
    svg: d3.Selection<null, unknown, null, undefined>,//d3.Selection<SVGGElement,unknown,null,undefined>,
    title:string,
    xlabel:string,
    ylabel:string,
    xScale:any, //d3.AxisScale<d3.AxisDomain>
    yScale:any,
    width:number,
    height:number,
    axis_width:number,
    axis_height:number,
    margin_top:number,
    margin_left:number) : void {

    svg.append("text")
        .attr("x", width/2)
        .attr("y", -margin_top/3)
        .attr("font-size", "24px")
        .attr("text-anchor","middle")
        .text(title);
    
    svg.append("text")
        .attr("x", width/2)
        .attr("y", height + 2*margin_top/3)
        .attr("font-size", "16px")
        .attr("text-anchor","middle")
        .text(xlabel);
    svg.append("text")
        .attr("transform", function(d) {
            return "rotate(-90)" 
        })
        .attr("x", -height/2)
        .attr("y", -2*margin_left/3)
        .attr("font-size", "16px")
        .attr("text-anchor","middle")
        .text(ylabel);
    svg.append("g")
        .attr("transform", "translate(0," + (axis_height) + ")")
        .call(d3.axisBottom(xScale)
        //.tickFormat((d)=> xDataFormat(d)) //.getFullYear())
        .ticks(5));
    svg.append("g")
        .attr("transform", "translate(" + axis_width + ", 0)")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale));
  };

  static undefinedHandler (valToCheck: any, errVal : number) : number {
    if(valToCheck) 
      return valToCheck;
    return errVal;
  };
}

export default ChartUtils;