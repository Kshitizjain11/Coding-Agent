import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: "file" is not in the working dir'
        if not os.path.isfile(abs_file_path):
            return f"Error: {file_path} is not in the working dir"
        
        file_content_string = ""
        with open(abs_file_path, 'r') as f:
            # Read one extra character to detect truncation.
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS]
                file_content_string += f'\nFile {file_path} truncated at {MAX_CHARS} characters'
        return file_content_string
    except Exception as e:
        return f'Exception in reading file {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the contents of the given file in a string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory.",
            ),
        },
    ),
)