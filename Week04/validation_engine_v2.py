
"""
Sample trade used to test the validation engine.

This will later be replaced with trades loaded from CSV files.
"""

trade = {
    "TradeID": "T001",
    "LEI": "",
    "UTI": "UTI001",
    "Amount": -100
}


import json

def load_rules(filename):
    with open(filename) as file:
        rules = json.load(file)
    
    return rules

import os

BASE_DIR = os.path.dirname(__file__)

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

"""
Runs the validation engine for the sample trade
and displays all validation errors.
"""

errors = validate_trade(trade)

print(errors)

