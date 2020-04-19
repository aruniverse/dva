import React from "react";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Slider from "@material-ui/core/Slider";
import Typography from "@material-ui/core/Typography";

interface SliderCardProps {
  onChange: (event: any, value: number | number[]) => void;
  title: string;
  description: string;
  minVal: number;
  maxVal: number;
  defaultValue: number;
  labels: number[];
}

const SliderCard = ({
  onChange,
  title,
  description,
  minVal,
  maxVal,
  defaultValue,
  labels,
}: SliderCardProps) => {
  var marks = [];
  for (var i = 0; i < labels.length; i++) {
    marks.push({ value: i, label: String(labels[i] + "%") });
  }
  return (
    <Grid item lg={2}>
      <Card variant="outlined">
        <CardContent>
          <Typography id="discrete-slider-small-steps" gutterBottom>
            <b>{title}:</b>
          </Typography>
          <p>{description}</p>
          <Slider
            defaultValue={defaultValue}
            step={1}
            marks={marks}
            min={minVal}
            max={maxVal}
            onChange={onChange}
            valueLabelDisplay="auto"
          />
        </CardContent>
      </Card>
    </Grid>
  );
};

export default SliderCard;
