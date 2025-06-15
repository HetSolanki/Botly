import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(abs_working_dir, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"' 
    try:
        with open(target_file, 'r') as file:
            content = file.read(MAX_CHARS)
            if len(content) == MAX_CHARS:
                content += f"[...File '{file_path}' truncated at 10000 characters]"
            return content
    except Exception as e:
        return f"Error while reading file '{file_path}': {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file located within the hardcoded working directory, limited to a maximum number of characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the predefined working directory."
            ),
        },
    ),
)
