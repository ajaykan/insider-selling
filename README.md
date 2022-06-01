# Insider trading and security performance

**Premise**:
This project describes insider trading in the strictly legal sense where an insider of a company buys or sells shares on the open market. This differs from newsworthy 'insider trading' where an insider places a trade on information not yet made public. These instances of insider trading are legal and frequent, and I hope to see if any value can be derived by studying these pattern. I use public data involving insiders of a company buying/selling their personal holdings to assess their entry/exit timing ability, and examine the strength of correlation between the magnitude of insider trading and the overall profitability of the trade.

**Model assumptions:**
Extrapolated price appreciation data on various timescales with short and medium term timescales
Standardized returns to Russell 2000 over same timeframe
Did not include dividend income over timescale
Discard data from securities that were delisted in the designated timeframe

**Process**:
Extracted instances from public dataset (ex. https://www.reddit.com/r/StockMarket/comments/afz2fw/significant_insider_trading_activity_last_7_days/)
Computed price appreciation/depreciation from time of trade to various timescales (6-24 months)
Standardized returns to SPY over same time period (trade return % / SPY return %) 
- For insider selling, returns were negated to signify selling
To get an aggregaate of an instance of insider trading, I took the average of the above computation accross all 2-3 timescales

Plotted deviations to see shape of distribution
Plotted deviation vs magnitude of trade (in dollars), to establish correlation

**Results**:
58% of insider buying trades outperformed IWM over the time frame [6, 12, 24] (in months) with an average deviation of 0.041; this would indicate that, on average, trades yielded 4.1% of the returns of IWM over similar timeframes

29% of insider selling trades outperformed IWM over the time frame [6, 12, 24] with an average deviation of -1.54; the magnitude of the price _appreciation_ in the sold assets exceeded returns of IWM by 54%, on average. 

**Flaws**:
The result of an individual security is highly volatile whereas a market or index generally follows a steady uptrend over time. This is why we saw the results of insider buying, in which 58% of trades ourperformed IWM, but because of the high amount of losers, the average return is a fraction of IWM returns.

Many of these securities had a small market cap (<1b) and went insolvent during the longer timeperiods. This is simply a testament to the quality of each datapoint involved.

**Improvements and extensions**:
Weight 'higher quality' securities more heavily; trading of these securities might offer more insight
Compute market adjusted returns by sector as opposed to a broad index; much of my data involved small cap pharmaceuticals

**Conclusion**:
The results indicate, as I suspected, that market returns are highly variable and are largely unpredicable. Betting on companies using insider trading data is unadvisable. In fact, as the data would indicate, taking a long position in a company which an insider reduced his position in would yield better returns than investing in the broad market. 
