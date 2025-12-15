def backtest(df):
    balance = 10000.0
    position = 0.0
    equity_curve = []

    for i in range(1, len(df)):
        price = df["Close"].iloc[i]
        rsi = df["RSI"].iloc[i]

        if rsi < 30 and position == 0:
            position = balance / price
            balance = 0

        elif rsi > 70 and position > 0:
            balance = position * price
            position = 0

        equity = balance + position * price
        equity_curve.append(round(equity, 2))

    return {
        "equity_curve": equity_curve,
        "final_equity": round(equity_curve[-1], 2),
        "profit": round(equity_curve[-1] - 10000, 2)
    }
