import json

import functions

response = ""
# Get task
initial_task_input = input("Give a task: ")

# Ollama/model initialization
model = "gemma3:4b"

response = functions.prompt_model(model, initial_task_input)
cleaned_response = response.replace("```", "").strip()
cleaned_response = cleaned_response.replace("json", "")
print(f"cleaned_response: {cleaned_response}")


result = None
done = False
iteration = 0
while not done:
    if iteration == 0:
        result = initial_task_input

    response = functions.prompt_model(model, result)
    cleaned_response = response.replace("```", "").strip()
    cleaned_response = cleaned_response.replace("json", "")
    print(f"cleaned_response: {cleaned_response}")

    try:

        data = json.loads(cleaned_response)
        function_name = data["function_name"]
        parameters = data["parameters"]

        if function_name == "print_to_user":
            if parameters["message"] == '0':
                done = True
        else:
            result = functions.execute_function(function_name, parameters)

    except json.JSONDecodeError as e:
        print(f"Error decoding response {e}")
        print(f"Response: {cleaned_response}")

    iteration += 1


# while not task_done:
#   split_response = response.split(" ")

#  for word in split_response:
#     print(word)

# if DONE_TOKEN in output:
#   task_done = True
