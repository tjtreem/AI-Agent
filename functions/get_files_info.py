import os


def get_files_info(directory=".", working_directory="./calculator"):

    abs_working_dir = os.path.abspath(working_directory)
    full_directory_path = os.path.join(abs_working_dir, directory)
    abs_directory = os.path.abspath(full_directory_path)

        
    if not abs_directory.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
    
    try:

        names = os.listdir(abs_directory)
        lines = []

        for name in names:
            full_path = os.path.join(abs_directory, name)
            size = os.path.getsize(full_path)
            is_directory = os.path.isdir(full_path)
            formatted_line = f"- {name}: file_size={size} bytes, is_dir={is_directory}"
            lines.append(formatted_line)

        result = "\n".join(lines)
        return result

    except Exception as e:
        return f"Error: {str(e)}"

