import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'     
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command = ["python3", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(
            command, 
            timeout=30, 
            text=True,
            capture_output=True,
            cwd=abs_working_directory
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")

        if result.stderr:
            output.append(f"STDERR: {result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"