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
