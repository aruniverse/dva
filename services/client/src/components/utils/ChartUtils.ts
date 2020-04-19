import * as d3 from "d3";

export class ChartUtils {
  static initChart(
    svg: d3.Selection<null, unknown, null, undefined>,
    title: string,
    xlabel: string,
    ylabel: string,
    xScale: any,
    yScale: any,
    width: number,
    height: number,
    axis_width: number,
    axis_height: number,
    margin_top: number,
    margin_left: number
  ): void {
    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", -margin_top / 3)
      .attr("font-size", "24px")
      .attr("text-anchor", "middle")
      .text(title);

    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", height + (2 * margin_top) / 3)
      .attr("font-size", "16px")
      .attr("text-anchor", "middle")
      .text(xlabel);
    svg
      .append("text")
      .attr("transform", function (d) {
        return "rotate(-90)";
      })
      .attr("x", -height / 2)
      .attr("y", (-2 * margin_left) / 3)
      .attr("font-size", "16px")
      .attr("text-anchor", "middle")
      .text(ylabel);
    svg
      .append("g")
      .attr("transform", "translate(0," + axis_height + ")")
      .call(d3.axisBottom(xScale).ticks(5));
    svg
      .append("g")
      .attr("transform", "translate(" + axis_width + ", 0)")
      .attr("class", "y axis")
      .call(d3.axisLeft(yScale));
  }

  static undefinedHandler(valToCheck: any, errVal: number): number {
    if (valToCheck) return valToCheck;
    return errVal;
  }

  static createLegend(
    svg: d3.Selection<null, unknown, null, undefined>,
    legendData: any[],
    width: number,
    height: number
  ) {
    const yOffsetInc = 25;
    const radius = 6;
    var yOffset = height - (legendData.length + 1) * yOffsetInc;

    //legend
    legendData.forEach((d) => {
      if (d["isLine"]) {
        var line2 = d3
          .line()
          .x(function (d) {
            return d[0];
          })
          .y(function (d) {
            return d[1];
          })
          .curve(d3.curveMonotoneX);

        var dataset: [number, number][] = [
          [20, yOffset],
          [30, yOffset],
        ];
        svg
          .append("path")
          .datum(dataset)
          .style("stroke", d.color)
          .attr("stroke-width", 3)
          .style("fill", "none")
          .attr("d", line2);
      } else {
        svg
          .append("circle")
          .attr("cx", 25)
          .attr("cy", yOffset)
          .attr("r", radius)
          .style("fill", d.color)
          .style("stroke", d.color);
        if (d["hollow"]) {
          svg
            .append("circle")
            .attr("cx", 25)
            .attr("cy", yOffset)
            .attr("r", (2 * radius) / 3)
            .style("fill", "white")
            .style("stroke", "white");
        }
      }
      svg
        .append("text")
        .attr("x", 35)
        .attr("y", 5 + yOffset)
        .text(d.name)
        .style("font-size", "12px")
        .attr("alignment-baseline", "middle");
      yOffset += yOffsetInc;
    });
  }
}
