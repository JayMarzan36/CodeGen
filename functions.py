import ollama


def prompt(model: str, message: str) -> str:
    prompt = f"""
    You are a code execution engine that receives a user request and translates it into a Python function call. Your output should be a JSON string.

    The JSON object MUST contain the following keys:

    * 'function_name' : (string) The name of the function to call.
    * 'parameters' : (dictionary) A dictionary of parameter names and their corresponding values.


    Valid functions you are able to call are the following

    * print_to_user : Print a message to the user.
        * print_to_user parameters : In order its a message variable that is a string.

    * prompt : Prompt the model and return a response as a string.
        * prompt parameters : In order its a model variable that is a string and a message variable that is a string.


    Example:

    User Request: "Calculate the area of a circle with radius 5."

    JSON Output:
    {{
      "function_name": "calculate_circle_area",
      "parameters": {{
        "radius": 5
      }}
    }}

    User Request: "Convert 100 USD to EUR"
    JSON Output:
    {{
      "function_name": "convert_currency",
      "parameters": {{
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
      }}
    }}

    User Request:  {message}
    JSON Output:
    """
    response: ollama.ChatResponse = ollama.chat(model=model, messages=[{
        'role': 'user',
        'content': prompt,
    }])

    return response['message']['content']


def print_to_user(message: str):
    print(f"{message}")


def test_calc(a: int, b: int) -> int:
    return a * b


FUNCTION_DICT = {
    "print_to_user": print_to_user,
    "prompt": prompt
}


def execute_function(function_name, parameters):
    if function_name == "print_to_user":
        print_to_user(parameters["message"])
    elif function_name == "prompt":
        prompt(parameters["model"], parameters["message"])
    else:
        print(f"Unkown function {function_name}")
