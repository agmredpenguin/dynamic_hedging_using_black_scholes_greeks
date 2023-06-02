# dynamic_hedging_with_black_scholes_greeks
Backtrader Backtest - Dynamic Hedging with Black Scholes Greeks

In this repo I've done two backtests both dynamic delta hedging using backtrader.

## First backtest: Hedge using underlying and Call contract

#### Hedging with Call contract - Strategy Explained
1.   We want to start by taking a long position in the Call contract
2.   Next, we want to use the current delta and short certain number of underlyings (SPY)
3.   Further, we check our positions at every mintues interval and re-hedge our position if required. 
4.   For example, if the delta in the beginning was 0.10 and after 30 mins it is 0.11, we need to short one more SPY contract to achieve a dynamic hedge. 
5.   Else, if after 30 mins, the delta becomes 0.8, we need to buy 2 SPY contracts to hold only 8 SPY positions 


## Second backtest: Hedge using underlying and Put contract

#### Lets try hedging with Put contract - Strategy Explained
1.   We want to start by taking a long position in the put contract
2.   Next, we want to use the current delta and long certain number of underlyings (SPY)
3.   Further, we check our positions at every 30 mintues interval and re-hedge our position if required. 



