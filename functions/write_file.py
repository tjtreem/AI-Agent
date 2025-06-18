import os


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    full_file_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_file_path)
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        
        directory_path = os.path.dirname(abs_file_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        
  
        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {str(e)}'
