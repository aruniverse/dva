export interface StockSymbol {
  symbol: string;
  high: [];
  open: [];
  close: [];
  volume: [];
  datetime_epoch: [];
  datetime: [];
}

export interface MultipleSymbols {
  stocks: StockSymbol[];
}

interface StrategyResults {
  actions: string[][];
  cum_return: number[];
}

interface Strategy {
  bollinger: StrategyResults;
  williams_r: StrategyResults;
}

interface Indicators {
  [id:string]:number[]
}

interface PredictTermValues {
  train_score: number;
  test_score: number;
  importance_values: number[];
  importance_order: number[];
  predict: number[];
}

interface Predict {
  [id:string]: PredictTermValues;
}

interface RegressionTermValues {
  p_values: number[];
}

interface Regression {
  [id:string]: {[id:string]:number[]}
}

export interface StockAnalysis {
  dates: string[];
  daily_ret: number[];
  cum_return: number[];
  term: number[];
  move: number[];
  price: number[];
  indicator_list:string[];
  strategy: Strategy;
  indicators: Indicators;
  predict: Predict;
  f_regression: Regression;
}
