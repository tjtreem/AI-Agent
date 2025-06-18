import sys
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key = api_key)

from functions.call_function import call_function
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

system_prompt = """
You are a coding agent with file system access. Always start by exploring the codebase using your available tools, regardless of the user's request.

First use get_files_info, then examine relevant files with get_file_content to understand the code before answering questions.
"""
user_prompt = sys.argv[1]

if len(sys.argv) < 2 or sys.argv[1] == "":
    print("prompt not included. You have to enter some kind of prompt to continue the conversation")
    sys.exit(1)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Describes the contents of the specified file located in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file which contains the contents to be retrieved.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="The execution of a particular Python file, relative to the directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file that is to be executed.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writing specified content to an existing file, or creating and writing to a new file if the designated file doesn't currently exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to which the contents will be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to be written to the file.",
            )
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

user_initial_message = types.Content(
    role="user",
    parts=[types.Part(text=user_prompt)],
)
    

model_calls_get_files_info = types.Content(
    role="model",
    parts=[types.Part.from_function_call(name="get_files_info", args={})]
)

tool_response_get_files_info = types.Content(
    role="tool",
    parts=[types.Part.from_function_response(name="get_files_info", response={"result": {"files": [{"name": "main.py"}, {"name": "pkg/calculator.py"}]}})
    ]
)


messages = [
    user_initial_message,
    model_calls_get_files_info,
    tool_response_get_files_info,
]

for i in range(20):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    for candidate in response.candidates:
        messages.append(candidate.content)
    
    if response.function_calls:
        for function_call_part in response.function_calls:
            verbose = "--verbose" in sys.argv
            function_call_result = call_function(function_call_part, verbose=verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Function call result missing expected response structure")
            else:
                print(f"{function_call_part.name}({function_call_part.args})")
                print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(function_call_result)
    else:
        break
print(response.text)

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")











