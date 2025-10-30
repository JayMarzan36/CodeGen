import json

import utils
from template import Template

response = ""
# Get task
# user_project = input("Whats the project? : ")
user_project = "I want to make a test library to help test out my code"
# Ollama/model initialization
# TODO: get list of models available and allow user to choose
model = "gemma3:4b"


# prompt the model to select the best user defined template to use given the user project
# Get user Templates
user_templates = utils.get_user_templates()

output_format = "{'template_name' : 'Template name here', 'justification' : 'A brief explanation of why you selected this template'}"

prompt_for_model = f"""
You are a project template selector. Your goal is to choose the best template from a library of templates to match the user's project description.

Available Templates are:
        {user_templates}

User Description: {user_project}

Choose the best template from the library and explain your reasoning. Return your response in the following JSON format:
    {output_format}
"""

response = utils.prompt_model(model, prompt_for_model)
cleaned_response = response.replace("```", "").strip()
cleaned_response = cleaned_response.replace("json", "")

try:
    data = json.loads(cleaned_response)
    template_name = data['template_name']

    if "." in template_name:
        template_name = template_name + "json"

    reason = data['justification']

    print(f"Template Name: {template_name}")
    print(f"Reason: {reason}")

    template = Template(f"templates/{template_name}")

    print("Template object made")

    template.makeFromTemplate()

    file_names = template.file_dict

    num_files = file_names.keys()

    current_file_name = ""
    current_file_path = ""

    for i in range(0, len(num_files), 1):
        current_file_name = num_files[i]
        current_file_path = file_names.get(current_file_name)

        file_prompt = f"""
                You are an expert code generator. Your goal is to generate boilerplate code for a project based on a given file name and a project description.

                Available File: [File Name: {current_file_name}]

                Project Description: {user_project}
                Generate the code for [“{current_file_name}”], incorporating the project description and creating a functional, basic application.  Return the code as a single, multi-line string, properly formatted.
        """

        code_response = utils.prompt_model(model, file_prompt)

        utils.write_to_file(current_file_path, code_response)


except json.JSONDecodeError as e:
    print(f"Error decoding response {e}")
    print(f"Response: {cleaned_response}")
