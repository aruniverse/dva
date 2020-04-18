import ScatterChart from "../d3/ScatterChart";
import LineChart from "../d3/LineChart";
import React, { useState } from "react";
import Grid from "@material-ui/core/Grid";
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Select from '@material-ui/core/Select';
import Slider from '@material-ui/core/Slider';
import Typography from '@material-ui/core/Typography';
import DoubleHorizontalBarChart from "../d3/DoubleHorizontalBarChart";
import SliderCard from "../ui/SliderCard";
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';

interface StringBoolean {
    [id:string]:boolean
}

const Indicators = (props: any) => {

    const dates : string[] = props.data.dates;
    const f_regression : {[id:string]: {[id:string]:number[]}} = props.data.f_regression;
    const predict : {[id:string]: {[id:string]:number[]}} = props.data.predict;
    const indicators : {[id:string]: {[id:string]:number[]}} = props.data.indicators;
    const cumReturn : number[] = props.data.cum_return;

    var final : JSX.Element[] = [];
    var term :any = 'term_5';
    var doubleData = [];
    var key = "fasdklj";
    var keyPlot = 1098;
    var termType : string = "term_5";
    const p_values : string = "p_values";
    
    var labels : string[] = [];
    Object.entries(indicators).forEach(
        ([key,value]) => {
            labels.push(key);
        }
    );

    const [predictionTerm, updateTerm] = useState(5);
    const [state, setState] = useState<StringBoolean[]>(labels.map(function(val:string) {return {val:true}}));
    
    const handleChange = (event: any, value: number | number[])  => {
        if(typeof(value)=="number") {
            updateTerm(value);
        }
    };

    const handleCheckBoxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setState({ ...state, [event.target.name]: event.target.checked });
      };

    const addGridOfX = (val:number) => {
        final.push(
            <Grid item lg={2}></Grid>
        );
    }


    addGridOfX(5);
    final.push(
        <div>
            <h1>Indicators</h1>
            <p>This page is used to determine which indicators are useful in a model to predict stock direction</p>
            <p>This plot shows indicators most likely to predict future stock direction</p>
        </div>
    );

    /******************* double bar chart *****************************/
    for(var i=0; i<f_regression[termType][p_values].length; i++) {
        doubleData.push([i,predict[termType]['importance_values'][i], f_regression[termType][p_values][i]]);
    };

    final.push(<Grid item lg={4} key={key}><Card variant="outlined"><DoubleHorizontalBarChart labels={labels} data={doubleData}></DoubleHorizontalBarChart></Card></Grid>)
    
    /*** slider + indicator card **********/
    const checkboxes = labels.map(function(val:string) { return <FormControlLabel control={<Checkbox checked={state[labels.indexOf(val)][val]} onChange={handleCheckBoxChange} name={val}></Checkbox>} label={val}></FormControlLabel>});

    final.push(
        <Grid item lg={2}>
            <Card>
                <FormControl component="fieldset">
                    <FormLabel component="legend">Select Indicators</FormLabel>
                    <FormGroup>
                        {checkboxes}
                    </FormGroup>
                </FormControl>
            </Card>
        </Grid>
    );

    final.push(SliderCard(handleChange, "Enter prediction term", "Select term to compare gain vs indicator", 1,60,1, []));

    /*** Scatter Plots ****************** */
    keyPlot++;

    addGridOfX(5);
    addGridOfX(5);
    addGridOfX(5);
    addGridOfX(5);
    addGridOfX(5);
    
    Object.entries(indicators).forEach(
        ([key,value]) => {
            var scatterData : any[][] = [];
            for(var i=0; i<dates.length-predictionTerm; i++) {
                scatterData[i] = [];
                scatterData[i].push(cumReturn[i+predictionTerm] - cumReturn[i]);
                scatterData[i].push(value[i]);
            }
            final.push(<Grid item lg={4} key={key}><Card variant="outlined"><ScatterChart data={scatterData} label={key}></ScatterChart></Card></Grid>);
            keyPlot++;
        }
    );

    return (
        <div><Grid container spacing={1}>{final}</Grid></div>
    );

}

export default Indicators;
