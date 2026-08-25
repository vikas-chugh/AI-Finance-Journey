



""" 

\Test to call LLM\


There are only four genuinely new pieces:

1. from openai import OpenAI -- Imports the SDK We just installed.

2. client = OpenAI() ---Creates our API client. It automatically uses the OPENAI_API_KEY environment variable.

3. client.responses.create(...) --Sends the request to the model.

4. response.output_text --Extracts the generated text from the response.

"""




from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    input="""
    You are a trade operations assistant.

    A derivative trade failed validation because its UTI is missing.

    Explain the validation failure in no more than two sentences.
    Do not introduce any regulatory requirements that were not provided.
    """
)

print(response.output_text)


"""
Response received-- 

The trade failed validation because its UTI (Unique Transaction Identifier) is missing. 
A UTI is required to validate and process the derivative trade.

 """