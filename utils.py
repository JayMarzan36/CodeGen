import os
import ollama


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
        print(f"Error: Folder '{folder_path}' not found")
        return []
