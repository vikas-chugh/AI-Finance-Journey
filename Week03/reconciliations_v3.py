"""
Project 1_V3: Trade Reconciliation Engine (Version 1)

Author: Vikas Chugh

Description:
Description:
Reads trade data from CSV files, reconciles internal and external trades,
and generates a reconciliation report that is displayed on the console
and saved to a text file.
"""

import csv
import os

def load_trades(filename):
    """
    Loads trades from a CSV file and returns
    a list of trade dictionaries.
    """
    trades = []

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        for trade in reader:
            trade["Amount"] = int(trade["Amount"])
            trades.append(trade)
    
    return trades


"""
Assigns the trade files to the function and provides the path 
where those files need to be looked at
"""

BASE_DIR = os.path.dirname(__file__)

internal_file = os.path.join(BASE_DIR, "internal_trades.csv")
external_file = os.path.join(BASE_DIR, "external_trades.csv")

internal_trades = load_trades(internal_file)
external_trades = load_trades(external_file)

"""

    Creates a dictionary for the a table, indexed by TradeID for the respective trades.
    """

def build_lookup(trades):
    trade_dict = {}
    for trade in trades:
        trade_dict[trade["TradeID"]] = trade
    return trade_dict

internal_trades_dict = build_lookup(internal_trades)
external_trades_dict = build_lookup(external_trades)

"""
    Compares key fields between an internal and external trade.
    Returns a list of all mismatched fields.
    """

def compare_trade(internal_trade, external_trade): #compares the attributes in internal and external lists
    mismatches = []
    if internal_trade["LEI"] != external_trade["LEI"]:
        mismatches.append("LEI Mismatch")
    if internal_trade["UTI"] != external_trade["UTI"]:
        mismatches.append("UTI Mismatch")
    if internal_trade["Amount"] != external_trade["Amount"]:
        mismatches.append("Amount Mismatch")
    return mismatches

"""
    Generates the reconciliation report by identifying:
    - Matched trades
    - Trades with field mismatches (exceptions)
    - Trades missing in the external system
    - Trades missing in the internal system

    Returns all four report sections.
    """

def generate_report():
    exceptions = []
    missing_in_internal = []
    missing_in_external = []
    matches = []

    # Loop 1
    for internal_trade in internal_trades:

        external_trade = external_trades_dict.get(
            internal_trade["TradeID"]
        )

        if external_trade is None:
            missing_in_external.append(internal_trade["TradeID"])
        else:
            mismatches = compare_trade(internal_trade, external_trade)

            if not mismatches:
                matches.append(internal_trade["TradeID"])
            else:
                exceptions.append(
                    {
                        "TradeID": internal_trade["TradeID"],
                        "Breaks": mismatches
                    }
                )

    # Loop 2
    for external_trade in external_trades:

        internal_trade = internal_trades_dict.get(
            external_trade["TradeID"]
        )

        if internal_trade is None:
            missing_in_internal.append(external_trade["TradeID"])

    return (
        matches,
        exceptions,
        missing_in_external,
        missing_in_internal
    )
"""
    Displays the reconciliation report in a readable format.
    """




def create_report(matches, exceptions,
                  missing_in_external,
                  missing_in_internal):
    report = ""
    report += "="*20 +"\n"
    report += "TRADE RECONCILIATION REPORT\n"
    report += "="*20
    report += "\n"
    report += "Matched Trades\n"
    report += "-" * 20 + "\n"
    for match in matches:
        report += str(match) + "\n"

    report += "\n"
    report += "Exceptions\n"
    report += "-" * 20 + "\n"

    for exception in exceptions:
        report += exception["TradeID"] + "\n"

        for break_type in exception["Breaks"]:
            report += f"   - {break_type}\n"
    report += "\n"
    report +="Missing in Internal\n"
    report +="-"*20 + "\n"

    for missing_internal in missing_in_internal:
        report += missing_internal+ "\n"
    report += "\n"
    
    report +="Missing in External\n"
    report +="-"*20 + "\n"

    for missing_external in missing_in_external:
        report += missing_external + "\n"
    
    return report


if __name__ == "__main__":

    matches, exceptions, missing_in_external, missing_in_internal = generate_report()

    report = create_report(
        matches,
        exceptions,
        missing_in_external,
        missing_in_internal
    )

    print(report)

    report_file = os.path.join(BASE_DIR, "report.txt")
    with open(report_file, "w") as file:
        file.write(report)
