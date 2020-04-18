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
import { StockAnalysis } from "../../types";

interface StringBoolean {
    [id:string]:boolean
}

const IndicatorsLayout = (props: StockAnalysis) => {

    var final : JSX.Element[] = [];
    var term :any = 'term_5';
    var doubleData = [];
    var key = "fasdklj";
    var keyPlot = 1098;
    var termType : string = "term_5";
    const p_values : string = "p_values";
    
    var labelStrings : string[] = [];
    var labels : StringBoolean = {};
    Object.entries(props.indicators).forEach(
        ([key,value]) => {
            labels[key] = true;
            labelStrings.push(key);
        }
    );

    const [predictionTerm, updateTerm] = useState(5);

    const [state, setState] = useState<StringBoolean>(labels);
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
        <Grid item lg={4}>
            <h1>Indicators</h1>
            <p>This page is used to determine which indicators are useful in a model to predict stock direction</p>
            <p>This plot shows indicators most likely to predict future stock direction</p>
        </Grid>
    );

    /******************* double bar chart *****************************/
    for(var i=0; i<props.f_regression[termType][p_values].length; i++) {
        doubleData.push([i,props.predict[termType]['importance_values'][i], props.f_regression[termType][p_values][i]]);
    };

    final.push(<Grid item lg={4} key={key}><Card variant="outlined"><DoubleHorizontalBarChart labels={labelStrings} data={doubleData}></DoubleHorizontalBarChart></Card></Grid>)

    addGridOfX(2);
    addGridOfX(2);
    addGridOfX(2);
    
    /*** slider + indicator card **********/

    const checkboxes = labelStrings.map(function(val:string) { return <FormControlLabel control={<Checkbox checked={state[val]} onChange={handleCheckBoxChange} name={val}></Checkbox>} label={val}></FormControlLabel>});

    final.push(
        <Grid item lg={2}>
            <Card variant="outlined">
                <FormControl component="fieldset">
                    <FormLabel component="legend">Select Indicators</FormLabel>
                    <FormGroup>
                        {checkboxes}
                    </FormGroup>
                </FormControl>
            </Card>
        </Grid>
    );


    final.push(SliderCard(handleChange, "Enter prediction term", "Select term to compare gain vs indicator", 1,props.dates.length-5,1, []));

    /*** Scatter Plots ****************** */
    keyPlot++;

    addGridOfX(5);
    addGridOfX(5);
    addGridOfX(5);
    //console.log(labels);
    console.log(state);
    
    Object.entries(props.indicators).forEach(
        ([key,value]) => {
            //console.log(labels.get(key));
            if(state[key]) {
                var scatterData : any[][] = [];
                for(var i=0; i<props.dates.length-predictionTerm; i++) {
                    scatterData[i] = [];
                    scatterData[i].push(props.cum_return[i+predictionTerm] - props.cum_return[i]);
                    scatterData[i].push(value[i]);
                }
                final.push(<Grid item lg={4} key={key}><Card variant="outlined"><ScatterChart data={scatterData} label={key}></ScatterChart></Card></Grid>);
                keyPlot++;
            }
        }
    );

    return (
        <div><Grid container spacing={1}>{final}</Grid></div>
    );

}

export default IndicatorsLayout;
