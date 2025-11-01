import os
import ollama
import time


def get_models() -> dict:
    response_list: ollama.ListResponse = ollama.list()
    model_dict = {}
    for model in response_list.models:
        model_dict[f"{model.model}"] = model
    return model_dict


def prompt_model(model: str, message: str) -> str:
    response: ollama.ChatResponse = ollama.chat(model=model, messages=[{
        'role': 'user',
        'content': message,
    }])
    return response['message']['content']


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


def get_user_templates(folder_path: str = "templates/"):
    try:
        file_names = [f for f in os.listdir(
            folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return file_names
    except FileNotFoundError:
        print("E\x1B[38;5;96mError: Folder '{folder_path}' not found\x1B[0m")
        return []


def loading_bar(percentage: int, message: str = "Percentage"):
    if not 0 <= percentage <= 100:
        print("\x1B[38;5;96mError: Percentage must be between 0 and 100.\x1B[0m")
        return

    bar_length = 50
    filled_length = int(bar_length * percentage / 100)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r\x1B[38;5;46m{message}: |{bar}| {percentage}%\x1B[0m', end='')

    while percentage < 100:
        time.sleep(0.05)
        percentage += 1

        filled_length = int(bar_length * percentage / 100)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        print(f'\r\x1B[38;5;46m{message}: |{
            bar}| {percentage}%\x1B[0m', end='')

    print()
