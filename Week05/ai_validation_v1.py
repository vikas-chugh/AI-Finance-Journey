"""Objective:
To create a resuable function to Convert an LLM response from unstructured prose into predictable machine-readable data"""


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


result = explain_validation_error(
    "T002",
    "UTI required for Derivative trades",
)

print(result)