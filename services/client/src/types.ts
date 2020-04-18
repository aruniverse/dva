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
  acc_dist_index: number[];
  chaikin_money_flow: number[];
  ease_of_move: number[];
  williams_r: number[];
  rel_strength: number[];
}

interface PredictTermValues {
  train_score: number;
  test_score: number;
  importance_values: number[];
  importance_order: number[];
  predict: number[];
}

interface Predict {
  indicator_list: string[];
  term_5: PredictTermValues;
  term_20: PredictTermValues;
  term_60: PredictTermValues;
}

interface RegressionTermValues {
  p_values: number[];
}

interface Regression {
  indicator_list: string[];
  term_5: RegressionTermValues;
  term_20: RegressionTermValues;
  term_60: RegressionTermValues;
}

export interface StockAnalysis {
  dates: string[];
  daily_ret: number[];
  cum_return: number[];
  term: number[];
  move: number[];
  strategy: Strategy;
  indicators: Indicators;
  predict: Predict;
  f_regression: Regression;
}
