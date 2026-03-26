import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check
    if not abs_file_path.startswith(abs_working_dir + os.sep):
        return 'Error: "file" is not in the working dir'

    parent_dir = os.path.dirname(abs_file_path)

    try:
        os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        return f'Could not create parent dirs: {parent_dir} = {e}'

    try:
        with open(abs_file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {abs_file_path} ({len(content)} characters written)"
    except Exception as e:
        return f"Failed to write to {abs_file_path},\n{e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an existing file or writes to a new file if it doesn't exist (and creates required parent dirs safely)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to write to the file as a string",
            ),
        },
    ),
)