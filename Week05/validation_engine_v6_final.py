"""
Project 2: Validation Engine - Version 6
Objective

Version 6 optimizes the AI explanation layer by avoiding repeated LLM calls for identical validation errors.

Instead of generating an explanation for every failed trade, the system:

identifies each unique validation error;
generates one AI explanation per unique error;
stores that explanation in a cache;
reuses it for every trade with the same error;
keeps TradeID handling inside deterministic Python code.
Key Design Principle

The AI explains the error type, while Python identifies the specific trade.

This makes the AI response reusable.
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

trade_file = os.path.join(BASE_DIR, "trades_v6.csv")

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

refer ai_validation_v1.py

------
explain_validation_error() IN v5 still accepts:

trade_id

That means the AI explanation may say:

"Add a UTI to trade T002."

If we reuse that explanation for T008, it could incorrectly still mention T002.

So for caching to be truly reusable, our next change should be:

explain_validation_error(error)

instead of:

explain_validation_error(trade_id, error)

The LLM should generate a generic explanation per error type:

"""

from openai import OpenAI
import json

client = OpenAI()


def explain_validation_error(error):

    response = client.responses.create(
        model="gpt-5.6-luna",

        instructions="""
        You are a trade operations assistant.

        Explain the validation failure using only the information provided.
        Do not invent regulatory or business requirements.
        Keep the explanation concise and operationally useful.
        """,

        input=f"""
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
                        "explanation": {
                            "type": "string"
                        },
                        "recommended_action": {
                            "type": "string"
                        }
                    },
                    "required": [
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

    explanation_cache = {}
    trade_explanations = []

    for result in results:
        if result["Errors"]:

            for error in result["Errors"]:

                if error not in explanation_cache:
                    print(f"Calling LLM for: {error}")
                    ai_result = explain_validation_error(error)

                    explanation_cache[error] = {
                        "explanation" : ai_result["explanation"],
                         "recommended_action": ai_result["recommended_action"]
                }

                    trade_explanations.append(
                    {
                        "trade_id": result["TradeID"],
                        "error": error,
                        "explanation": explanation_cache[error]["explanation"],
                        "recommended_action":explanation_cache[error]["recommended_action"]
                    }
            )

    return trade_explanations, explanation_cache

trade_explanations, explanation_cache = generate_ai_explanations(results)

# print(trade_explanations)
# print(explanation_cache)


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

def create_report(total, passed, failed, results, trade_explanations):
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
        report += f'{result["TradeID"]}\n'

        if result["Errors"]:
            report += "STATUS: FAILED\n"

            for error in result["Errors"]:
                report += f"Error: {error}\n"

                for explanation in trade_explanations:

                    if error == explanation["error"]:

                        report += "AI Explanation\n"
                        report += f'   - {explanation["explanation"]}\n'

                        report += "Recommended Action\n"
                        report += f'   - {explanation["recommended_action"]}\n\n'

                        break

        else:
            report += "STATUS: PASSED\n\n"

    return report

"""
Prints the report in the terminal and a text file separately
"""

report = create_report(total, passed, failed, results, trade_explanations)

print(report)


report_file = os.path.join(BASE_DIR, "report.txt")
with open(report_file, "w") as file:
    file.write(report)

