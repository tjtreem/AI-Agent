import os
import subprocess


def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    full_file_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_file_path)
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    try:
        
      
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(
                ["python3", abs_file_path], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                timeout=30, 
                cwd=abs_working_dir
            )

        if not result.stdout and not result.stderr:
            return "No output produced."


        stdout_text = f"STDOUT: {result.stdout.decode()}"
        stderr_text = f"STDERR: {result.stderr.decode()}"

        new_string = "\n".join([stdout_text, stderr_text])

        if result.returncode != 0:
            new_string += f"\nProcess exited with code {result.returncode}"


        return new_string

    except Exception as e:
        return f"Error: executing Python file: {e}"



  



