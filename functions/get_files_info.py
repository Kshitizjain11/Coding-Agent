import os
from google.genai import types

def get_files_info(working_directory,directory=None):
    abs_wor_dir = os.path.abspath(working_directory)
    abs_dir = ""
    if directory is None:
        abs_dir = os.path.abspath(os.path.join(working_directory))
    else :
        abs_dir = os.path.abspath(os.path.join(working_directory,directory))
    
    if not abs_dir.startswith(abs_wor_dir):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

    if not os.path.isdir(abs_dir):
        return f"Error: '{directory}' is not a directory"
    
    final_response = ""
    contents = os.listdir(abs_dir)
    for content in contents:
        content_path = os.path.join(abs_dir,content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        final_response += f"- {content}:file_size={size}, is_dir={is_dir}\n"
    return final_response

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

    