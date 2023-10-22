import subprocess

def executePython(user_code):
    with open("temp_code.py", "w") as temp:
        temp.write(user_code)

    try:
        # Run the user's code and capture the output
        output = subprocess.check_output(["python", "temp_code.py"], stderr=subprocess.STDOUT, timeout=10).decode('utf-8')
        return output
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')  # return the error
    except subprocess.TimeoutExpired:
        return "Execution timed out!"
