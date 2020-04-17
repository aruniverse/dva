import React from "react";
import withMainContainer from "../main/MainContainer";
import * as d3 from "d3";

const Line = () => {
  //   const drawLine = (): JSX.Element => {
  //     const xScale = () =>
  //       d3
  //         .scaleTime()
  //         .domain(d3.extent(this.props.data, ({ date }) => date))
  //         .rangeRound([0, this.props.width]);

  //     const yScale = () =>
  //       d3
  //         .scaleLinear()
  //         .domain(d3.extent(this.props.data, ({ value }) => value))
  //         .rangeRound([this.props.height, 0]);

  //     const line = () =>
  //       d3
  //         .line()
  //         .x(d => xScale(d.date))
  //         .y(d => yScale(d.value));

  //     return <path className="line" d={line(this.props.data)} />;
  //   };

  return (
    <div>
      {/* <svg
        className="line-container"
        width={this.props.width}
        height={this.props.height}
      >
        {drawLine()}
      </svg> */}
    </div>
  );
};

export default withMainContainer(Line);
