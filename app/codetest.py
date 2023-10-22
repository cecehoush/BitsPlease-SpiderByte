def test_user_code(user_code, test_cases):
    results = []
    
    for test_case in test_cases:
        function_name = test_case.test_function
        # Assuming the input is comma-separated, we can convert it to a list of arguments
        args = test_case.input.split(',')
        expected_output = test_case.required_output
        
        # Construct the full code to execute
        args_str = ', '.join(args)
        full_code = f"{user_code}\nresult = {function_name}({args_str})"
        
        context = {}
        exec(full_code, context)
        result = context.get("result")

        # Compare result with expected output
        results.append(str(result) == expected_output)  # Convert result to string for comparison, if needed

    return results
