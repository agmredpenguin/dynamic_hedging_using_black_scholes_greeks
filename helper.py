import pandas as pd
import mplfinance as mpl
import matplotlib.pyplot as plt

def get_indicators(strats, input_data, csv_name = None):
    '''
    Function to get the indicators and prices into a dataframe and also store to a csv.

    Note: in the backtest, the variable names of the indicators should be prefixed with *vr_*.

    Inputs 
    strats: result of backtest
    input_data (list): list of dataframes with input data of multiple timeframes 
    '''
    global strat_res 
    strat_res = strats[0]

    inp_data = []
    for data in input_data:
        inp_data.append(data)

    names = [ele for ele in dir(strat_res) if "vr_" in str(ele)]
    res = [eval(f"strat_res.{ele}.array") for ele in names]
    
    names = [ele.replace("vr_", "") for ele in names]
    results = []
    for dt in inp_data:
        for r in range(len(res)):
            if dt.shape[0] == len(res[r]):
                dt[names[r]] = res[r]
        results.append(dt)
    results.sort(key= len, reverse= True)

    Final = results.pop(0)
    for i in range(len(results)):
        Final = pd.merge(Final, results[i], "left", "datetime", suffixes=(f"_TF{i}", f"_TF{i+1}"))
        Final.fillna(method = "pad", inplace=True)
    
    if csv_name:
        Final.to_csv(f"{csv_name}.csv")
    del(strat_res)
    return Final

def get_trade_list(strats, csv_name= None):
    """
    Function to retrieve the trade details of the backtest

    Input:
    strats: output of the backtest
    csv_name: (default None) Name of the csv file
    """
    df_trade_list = strats[0].analyzers.getbyname("trade_list").get_analysis()
    df = pd.DataFrame(df_trade_list)
    if len(df) == 0:
      return df
      
    df["DateTimeIn"] = df['DateIn'].astype(str) + " " + df['TimeIn']
    df["DateTimeIn"] = pd.to_datetime(df["DateTimeIn"])
    df["DateTimeOut"] = df['DateOut'].astype(str) + " " + df['TimeOut']
    df["DateTimeOut"] = pd.to_datetime(df["DateTimeOut"])
    df.drop(['TradeIdentifier', 'Ticker', "DateIn", "TimeIn", "DateOut", "TimeOut" ], axis=1, inplace=True)
    if csv_name:
        df.to_csv(f"{csv_name}.csv")
    return df

def mlpplot(df_data, title = "Candle Sticke Chart", NRows = None):
    """
    Function to plot a candle stick chart chart
    Inputs:
    df_data: dataframe with datetime, open, high, low, close, volume columns
    title: title of the plot
    NRows: number of rows to plot 

    """

    if NRows:
        df_data = df_data.iloc[:NRows, :]

    df_data.set_index("datetime", inplace=True, drop=True)
    df_data.index = df_data.index.tz_localize(None)
    fig = mpl.plot(df_data,
         type="candle", 
         title = "SPY",  
        #  style="yahoo", 
         volume=False, 
         figratio=(12.00, 5.75),
         returnfig=True,
         show_nontrading=False,
    )
    plt.show()
    
    return fig
    
def get_summary_stats(df, to_print = False):
  """
  Get Summary statistics of the basktest.
  Returns dataframes of total stats, long stats, and short stats
  The output DF can be copied and pasted to the excel sheet  
  """
  def get_stats(df):
    totals_stats = {}
    if len(df) > 0:
      totals_stats['Total Trades'] = [df.shape[0]]
      totals_stats['Total PnL'] = [df['Profit|Loss'].sum()]
      # Wins
      totals_stats['No. of Wins'] = [df[df['Profit|Loss'] > 0].count()[0]]
      totals_stats['Total Profit'] = [df[df['Profit|Loss'] > 0]['Profit|Loss'].sum()]
      totals_stats['Max Profit'] = [df[df['Profit|Loss'] > 0]['Profit|Loss'].max()]
      totals_stats['Median Profit'] = [df[df['Profit|Loss'] > 0]['Profit|Loss'].describe()['50%']]
      totals_stats['Avg Profit'] = [df[df['Profit|Loss'] > 0]['Profit|Loss'].mean()]
      totals_stats['Std Profit'] = [df[df['Profit|Loss'] > 0]['Profit|Loss'].std()]
      totals_stats['Avg Trade Bars1'] = [df[df['Profit|Loss'] > 0]['TradeDurationBars'].mean()]
      #Losses
      totals_stats['No. of Losses'] = [df[df['Profit|Loss'] < 0].count()[0]]
      totals_stats['Total Loss'] = [df[df['Profit|Loss'] < 0]['Profit|Loss'].sum()]
      totals_stats['Max Loss'] = [df[df['Profit|Loss'] < 0]['Profit|Loss'].min()]
      totals_stats['Median Loss'] = [df[df['Profit|Loss'] < 0]['Profit|Loss'].describe()['50%']]
      totals_stats['Avg Loss'] = [df[df['Profit|Loss'] < 0]['Profit|Loss'].mean()]
      totals_stats['Std Loss'] = [df[df['Profit|Loss'] < 0]['Profit|Loss'].std()]
      totals_stats['Avg Trade Bars2'] = [df[df['Profit|Loss'] < 0]['TradeDurationBars'].mean()]
    return pd.DataFrame(totals_stats)

  totals_stats = get_stats(df)
  longs_stats = pd.DataFrame()
  shorts_stats = pd.DataFrame()
  if len(df):
    longs_stats = get_stats(df[df['OrderType'] == "long"])
    shorts_stats = get_stats(df[df['OrderType'] == "short"])

  if to_print:
    print("Totals")

    print(totals_stats.T)
    print()

    print("Longs")
    print(longs_stats.T)
    print()

    print("Shorts")
    print(shorts_stats.T)
    print()
  return totals_stats, longs_stats, shorts_stats