import json

import utils
from template import Template

# Get task
user_project = input("Whats the project? : ")

# Ollama/model initialization

model_dict = utils.get_models()

model_names = model_dict.keys()

print("Please select a model by inputing the whole name shown")

for i in model_dict.keys():
    print(f"\tModel  :  {i}")


model = input("What model to use: ")

# prompt the model to select the best user defined template to use given the user project
# Get user Templates
user_templates = utils.get_user_templates()

output_format = "{\"template_name\" :\"Template name here\", \"justification\" : \"A brief explanation of why you selected this template\"}"

prompt_for_model = f"""
You are a project template selector. Your goal is to choose the best template from a library of templates to match the user's project description.

Available Templates are:
        [{user_templates}]

User Description: {user_project}

Choose the best template from the library and explain your reasoning. Return your response in the following JSON format:
    {output_format}
"""

response = utils.prompt_model(model, prompt_for_model)
cleaned_response = response.replace("```", "").strip()
cleaned_response = cleaned_response.replace("json", "")
try:
    data = json.loads(cleaned_response)
    template_name = data["template_name"]
    if "." in template_name:
        template_name = template_name + "json"

    reason = data["justification"]

    print(f"Template Name: {template_name}")
    print(f"Reason: {reason}")


except json.JSONDecodeError as e:
    print(f"Error decoding response {e}")
    print(f"Response: {cleaned_response}")


template = Template(f"templates/{template_name}")

print("Template object made")

template.makeFromTemplate()

file_names = template.file_dict.keys()

current_file_name = ""
current_file_path = ""

languages = {
    "py": "python",
    "cpp": "cpp",
    "java": "java",
    "txt": "txt",
    "md": "md",
    ".js": "js",
    ".html": "html",
    ".css": "css"
}


for file in file_names:
    current_file_name = file
    file_extension = current_file_name.split(".")[1]
    current_file_path = template.file_dict.get(current_file_name)

    file_prompt = f"""
        Generate code for a project based on a given file name and a project description.

        Available File: {current_file_name}

        Project Description: {user_project}

        Generate the code for {current_file_name}, incorporating the project description and creating a functional, basic application.  Return the code as a single string.
        """
    code_response = utils.prompt_model(model, file_prompt)

    code_response = code_response.replace("```", "")
    language_keys = languages.keys()
    if file_extension in language_keys:
        code_response = code_response.replace(
            languages.get(file_extension), "")

    utils.write_to_file(current_file_path, code_response)

print("\x1B[38;5;46mComplete")
