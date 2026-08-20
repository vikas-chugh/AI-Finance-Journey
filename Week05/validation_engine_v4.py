"""
Project 2: Validation Engine - Version 4

Enhances V3 by adding conditional checks.
"""

import csv
import json
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
Loads trade data from a CSV file and returns
a list of trade dictionaries.
"""
def load_rules(filename):
    """Loads validation rules from a JSON file."""
    with open(filename) as file:
        rules = json.load(file)

    return rules


BASE_DIR = os.path.dirname(__file__)

trade_file = os.path.join(BASE_DIR, "trades.csv")

trades = load_trades(trade_file)

rules_file = os.path.join(BASE_DIR, "validation_rules.json")

RULES = load_rules(rules_file)


"""
Validates whether a required field contains a value.
Returns the configured error message if validation fails.
"""
def validate_required(trade, rule):
    value = trade[rule["field"]]
    if value.strip() == "":
        return rule["message"]
    return None


"""
Validates whether a numeric value in a trade meets the minimum
value defined in the validation rule.
"""
def validate_min(trade, rule):
    value = trade[rule["field"]]

    if value < rule["value"]:
        return rule["message"]
    return None
"""
Validates whether a trade meets conditional checks in the validation rules.
"""
def validate_conditional_required(trade, rule):
        if trade[rule["condition_field"]] == rule["condition_value"]:
            if trade[rule["field"]].strip() == "":
                return rule["message"]
        return None


"""
Maps each validation rule type to its corresponding
validator function.
"""
VALIDATORS = {
    "required": validate_required,
    "min": validate_min,
    "conditional_required": validate_conditional_required
}


"""
Validates a trade in the dataset and returns
the validation results.
"""
def validate_trade(trade):
    
    errors = []

    for rule in RULES:

        rule_type = rule["type"]

        validator = VALIDATORS[rule_type]

        error = validator(trade, rule)

        if error:
            errors.append(error)

    return errors


"""
Validates every trade in the dataset and returns
the validation results for each trade.
"""
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

"""
Calculates total, passed, and failed trade counts
from the validation results.
"""

def generate_summary(results):
    total = 0
    passed = 0
    failed = 0

    for result in results:
        total += 1

        if not result["Errors"]:
            passed += 1
        else:
            failed += 1

    return total, passed, failed

total, passed, failed = generate_summary(results)

"""
Creates a human-readable validation report from
the summary and individual trade results.
"""

def create_report(total, passed, failed, results):
    report = ""
    report += "="*20 +'\n'
    report += "TRADE VALIDATION REPORT" +'\n'
    report += "="*20
    report += "\n"
    report += f"Total Trades: {total}" + '\n'
    report += f"Passed Trades: {passed}" + '\n'
    report += f"Failed Trades: {failed}" + '\n'

    report +="-"*20 +'\n'

    for result in results:
        report += f'{result["TradeID"]+'\n'}'
        if result["Errors"]:
            report +="STATUS: FAILED" +'\n'
            for error in result["Errors"]:
                    report+=(f'   - {error}')
                    report+= '\n'
        else:
            report+="STATUS: PASSED" +'\n'
            report+= '\n'

    return report

"""
Creates a human-readable validation report from
the summary and individual trade results.
"""

report = create_report(total, passed, failed, results)

print(report)

report_file = os.path.join(BASE_DIR, "report.txt")
with open(report_file, "w") as file:
    file.write(report)

