

"""
Project 2 - Validation Engine (Version 1)

Author: Vikas Chugh

Description:
Builds a generic rule-based validation engine for financial trades.

Unlike the previous project where validation logic was hardcoded into
individual functions, this version stores validation rules as data.
The engine reads each rule, applies it dynamically to a trade, and
returns all validation errors.

Current Rule Types:
- required
- min


V1
- Introduced rule-based validation engine
- Supported required and minimum value validations
- Validated a single trade using configurable rules

Future Versions:
- Read rules from JSON
- Validate multiple trades from CSV
- Support additional rule types
- AI-powered validation explanations
"""


"""
Defines the validation rules for the engine.

Each rule specifies:
- field to validate
- validation type
- threshold/value (if required)
- error message

The engine reads these rules dynamically instead of using
hardcoded validation functions.
"""

RULES = [
    {
        "field": "TradeID",
        "type": "required",
        "message": "Missing TradeID"
    },
    {
        "field": "LEI",
        "type": "required",
        "message": "Missing LEI"
    },
    {
        "field": "UTI",
        "type": "required",
        "message": "Missing UTI"
    },
    {
        "field": "Amount",
        "type": "min",
        "value": 1,
        "message": "Invalid Amount"
    }
]

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


"""
Validates a single trade against all configured validation rules.

Loops through each rule, applies the appropriate validation,
and returns a list of all validation errors found.
"""

def validate_trade(trade):
    
    errors = []
# Apply each validation rule to the trade
    for rule in RULES:
# Read the field and its value from the current rule
        field = rule["field"]
        value = trade[field]
# Check mandatory fields
        if rule["type"] == "required":
            if value.strip() == "":
                errors.append(rule["message"])
# Check minimum numeric value
        if rule["type"] == "min":
            if int(value) < rule["value"]:
                errors.append(rule["message"])
    return errors


"""
Runs the validation engine for the sample trade
and displays all validation errors.
"""

errors = validate_trade(trade)

print(errors)
