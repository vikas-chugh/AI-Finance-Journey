"""
Project 2: Validation Engine - Version 5
Validation Engine V5 introduces an AI explanation layer on top of the existing deterministic validation system.

V4 remains responsible for:

applying validation rules;
determining PASS/FAIL;
identifying errors;
generating summary statistics and the validation report.

V5 adds:

sending failed validation errors to an LLM;
generating structured explanations;
recommending remediation actions;
keeping AI separate from deterministic validation decisions.
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

"""Objective:
To create a resuable function to Convert an LLM response from unstructured prose into predictable machine-readable data

refer ai_validation_v1.py"""

from openai import OpenAI
import json

client = OpenAI()


def explain_validation_error(trade_id, error):

    response = client.responses.create(
        model="gpt-5.6-luna",

        instructions="""
        You are a trade operations assistant.

        Explain the validation failure using only the information provided.
        Do not invent regulatory or business requirements.
        Keep the explanation concise and operationally useful.
        """,

        input=f"""
        Trade ID: {trade_id}

        Validation Error:
        {error}

    
        """,

        text={
            "format": {
                "type": "json_schema",
                "name": "validation_explanation",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "trade_id": {
                            "type": "string"
                        },
                        "explanation": {
                            "type": "string"
                        },
                        "recommended_action": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "trade_id",
                        "explanation",
                        "recommended_action"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(response.output_text)

"""Adds an AI summary for all errors in each trade"""

def generate_ai_explanations(results):

    explanations = []

    for result in results:
        if result["Errors"]:

            for error in result["Errors"]:
                explanation = explain_validation_error(
                    result["TradeID"],
                    error
                )

                explanations.append(explanation)

    return explanations

explanations = generate_ai_explanations(results)

print(explanations)


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
Prints the report in the terminal and a text file separately
"""

report = create_report(total, passed, failed, results)

print(report)


report_file = os.path.join(BASE_DIR, "report.txt")
with open(report_file, "w") as file:
    file.write(report)

