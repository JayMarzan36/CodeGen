import ollama


def prompt_model(model: str, message: str) -> str:
    prompt = f"""
    You are a code execution engine that receives a user request and translates it into a Python function call. Your output should be a JSON string.

    The JSON object MUST contain the following keys:

    * 'function_name' : (string) The name of the function to call.
    * 'parameters' : (dictionary) A dictionary of parameter names and their corresponding values.


    Valid functions you are able to call are the following

    * print_to_user : Print a message to the user.
        * print_to_user parameters : In order its a message variable that is a string.

    * prompt_model : Prompt the model and return a response as a string.
        * prompt parameters : In order its a model variable that is a string and a message variable that is a string.

    * create : Create a new empty file.
        * create parameters: In order its a file_name variable that is a string of the file_name that includes the extension.

    * write : Write to a file.
        * write parameters: In order its a file_name variable that is a string of the file_name that includes the extensions and a content variable that is a str that holds the contents that should be written to the file.

    After running a function or command you will either be prompted with a '0' or a '1'. A '0' means the function or command ran successfully, if its a '1' the funciton or command was unsuccessfull.

    If a function or command is ran successfully, meaning you were promted with a '0' you may move on to the next function or command needed to run to complete the task.

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


def print_to_user(message: str) -> int:
    print(f"{message}")
    return 0


def create_file(file_name: str) -> int:
    try:
        file = open(file_name, 'x')
        return 0
    except Exception as e:
        return 1


def write_to_file(file_name: str, content: str) -> int:
    try:
        with open(file_name, 'w') as file:
            file.write(content)
        return 0
    except Exception as e:
        return 1


def execute_function(function_name, parameters):
    result = None
    if function_name == "print_to_user":
        result = print_to_user(parameters["message"])
    elif function_name == "prompt_model":
        result = prompt_model(parameters["model"], parameters["message"])
    elif function_name == "create":
        result = create_file(parameters["file_name"])
    elif function_name == "write":
        result = write_to_file(parameters["file_name"], parameters["content"])
    else:
        print(f"Unkown function {function_name}")
    return result
