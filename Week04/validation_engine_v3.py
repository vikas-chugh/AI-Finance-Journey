
import csv

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


import json

def load_rules(filename):
    with open(filename) as file:
        rules = json.load(file)
    
    return rules


import os
BASE_DIR = os.path.dirname(__file__)

trade_file = os.path.join(BASE_DIR, "trades.csv")

trades = load_trades(trade_file)

rules_file = os.path.join(BASE_DIR, "validation_rules.json")

RULES = load_rules(rules_file)


def validate_required(value, rule):
    if value.strip() == "":
        return rule["message"]
    return None

def validate_min(value, rule):
    if value < rule["value"]:
        return rule["message"]
    return None

VALIDATORS = {
    "required": validate_required,
    "min": validate_min
}


def validate_trade(trade):
    
    errors = []

    for rule in RULES:

        field = rule["field"]

        value = trade[field]

        rule_type = rule["type"]

        validator = VALIDATORS[rule_type]

        error = validator(value, rule)

        if error:
            errors.append(error)

    return errors


def validate_all_trades(trades):

    results = []

    for trade in trades:

        errors = validate_trade(trade)

        results.append(
            {
                "TradeID": trade["TradeID"],
                "Errors": errors
            }
        )

    return results

results = validate_all_trades(trades)

print(results)

