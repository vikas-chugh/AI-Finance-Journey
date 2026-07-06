"""
Project 1: Trade Reconciliation Engine (Version 1)

Author: Vikas Chugh

Description:
Compares internal and external trade data to identify:
- Matched trades
- Field mismatches
- Trades missing in either system

This project demonstrates the use of:
- Functions
- Lists and dictionaries
- Nested loops
- Modular programming
- Basic reconciliation logic
"""



internal_trades = [
    {"TradeID": "T001", "LEI": "LEI001", "UTI": "UTI001", "Amount": 1000},
    {"TradeID": "T002", "LEI": "LEI002", "UTI": "UTI002", "Amount": 2500},
    {"TradeID": "T003", "LEI": "LEI003", "UTI": "UTI003", "Amount": 1500},
    {"TradeID": "T004", "LEI": "LEI004", "UTI": "UTI004", "Amount": 4000},
]

external_trades = [
    {"TradeID": "T001", "LEI": "LEI001", "UTI": "UTI001", "Amount": 1000},
    {"TradeID": "T002", "LEI": "LEI999", "UTI": "UTI002", "Amount": 2500},
    {"TradeID": "T003", "LEI": "LEI003", "UTI": "UTI999", "Amount": 1600},
    {"TradeID": "T005", "LEI": "LEI005", "UTI": "UTI005", "Amount": 800},
]

"""
    Searches for a trade by TradeID in the given trade list.
    Returns the matching trade dictionary if found, otherwise returns None.
    """

def find_trade(trade_id, trade_list): #Finds the trade in the tradelist
    for trade in trade_list:
        if trade["TradeID"] == trade_id:
            return trade
    
    return None

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

    for internal_trade in internal_trades:
        external_trade = find_trade(internal_trade["TradeID"], external_trades)

        if external_trade is None:
            missing_in_external.append(internal_trade["TradeID"])
        else:
            mismatches = compare_trade(internal_trade, external_trade)
            if not mismatches:
                matches.append(internal_trade["TradeID"])
            else:
                exceptions.append(
                    {
                        "TradeID":internal_trade["TradeID"],
                        "Breaks" : mismatches
                    }
                )
                                    
    for external_trade in external_trades:
        internal_trade = find_trade(external_trade["TradeID"], internal_trades)
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

def print_report(matches, exceptions, missing_in_external, missing_in_internal):
    print("="*20)
    print("TRADE RECONCILIATION REPORT")
    print("="*20)

    print()

    print("Matched Trades")
    print("-"*25)

    for match in matches:
        print(match)
    
    print()

    print("Exceptions")
    print("-"*25)

    for exception in exceptions:
        print(f'{exception["TradeID"]}')

        for break_type in exception["Breaks"]:
            print(f'   - {break_type}')      
        
    print()

    print("Missing in Internal")
    print("-"*25)

    for missing_internal in missing_in_internal:
        print(missing_internal)
    
    print()

    print("Missing in External")
    print("-"*25)

    for missing_external in missing_in_external:
        print(missing_external)

if __name__ == "__main__":

    matches, exceptions, missing_in_external, missing_in_internal = generate_report()

    print_report(
        matches,
        exceptions,
        missing_in_external,
        missing_in_internal
    )

    