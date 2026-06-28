trades = [
    {"TradeID": "T001", "Product": "Equity", "Quantity": 100, "Price": 250, "Country": "Singapore"},
    {"TradeID": "T002", "Product": "Bond", "Quantity": 50, "Price": 980, "Country": "UK"},
    {"TradeID": "T003", "Product": "ETF", "Quantity": 200, "Price": 120, "Country": "India"},
    {"TradeID": "T004", "Product": "Derivative", "Quantity": 10, "Price": 1500, "Country": "Hong Kong"},
]

print(len(trades))

for trade in trades:
    trade["TradeValue"] = trade["Quantity"] * trade["Price"]
print(trades)

for trade in trades:
    print(f" Trade {trade['TradeID']} Value = {trade['TradeValue']}")

Sum = 0
for trade in trades:
    Sum += trade["TradeValue"]
print(f"Total Portfolio Value = {Sum}")

print([trade["TradeID"] for trade in trades if trade["TradeValue"] == max(trade["TradeValue"] for trade in trades)])
print([trade["TradeID"] for trade in trades if trade["TradeValue"] == min(trade["TradeValue"] for trade in trades)])

