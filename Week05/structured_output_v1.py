
"""Objective

Convert an LLM response from unstructured prose into predictable machine-readable data"""



from openai import OpenAI
import json

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",

    instructions="""
    You are a trade operations assistant.
    Explain validation failures using only the information provided.
    Do not invent regulatory requirements.
    """,

    input="""
    Trade ID: T002
    Product: Derivative

    Validation Error:
    UTI required for Derivative trades

    Relevant Business Rule:
    Derivative trades require a UTI.
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

result = json.loads(response.output_text)

print(type(result))
print(result["trade_id"])
print(result["explanation"])
print(result["recommended_action"])