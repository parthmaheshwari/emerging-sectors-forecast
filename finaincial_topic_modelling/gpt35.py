import openai
openai.api_key = ""

"""
This Python script utilizes the OpenAI GPT-3 API to generate a response based on a given prompt. The response includes three keywords for each of the two specified companies, describing their respective research areas.

It uses the following libraries:
- openai: The OpenAI Python library for interfacing with the GPT-3 API.

The steps in the code are as follows:
1. Import the openai library and set the API key. Replace the empty string in 'openai.api_key' with your actual API key.
2. Create a completion request using the 'openai.Completion.create' method.
    - Specify the GPT-3 engine to use (e.g., "text-davinci-002").
    - Provide a prompt that instructs the model to generate three keywords for each of the two companies to describe their research areas. The prompt is written in plain English.
    - Set 'max_tokens' to limit the length of the response to 50 tokens.
3. Extract the generated text from the response.

Note: Ensure that you have a valid OpenAI API key and choose an appropriate engine for your specific use case.

Usage:
- Replace the empty string in 'openai.api_key' with your actual OpenAI API key.
- Run the script to send the prompt to the OpenAI GPT-3 API and receive a response containing keywords for the specified companies' research areas.
"""

response = openai.Completion.create(
    engine="text-davinci-002",  # Choose an appropriate engine
    prompt="Given a list of companies ['OpenAI','Meta']. Give 3 keywords for each company to describe which research areas each company falls under, as a python list of lists",
    max_tokens=50  # Set a limit on the length of the response
)

generated_text = response.choices[0].text