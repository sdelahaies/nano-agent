from typing import List, Dict, Any, Callable

def docstring_to_tool_definition(func,FUNCTION_REGISTRY):
    # TODO: check for optional parameters, here all arguments are considered as required
    import re
    docstring = FUNCTION_REGISTRY[func].__doc__
    function_name = func

    match = re.search(r'([^"]*)\nParameters:', docstring, re.DOTALL)
    if match:
        description_func = match.group(1).strip()
    else:
        description_func = ""

    # Extract the parameters section and parse it into a dictionary
    parameters_section = re.search(r'Parameters:\n([\s\S]*?)(?=\nReturns:|$)', docstring, re.DOTALL)
    if parameters_section:
        parameters_text = parameters_section.group(1)
        parameters = {}
        for line in parameters_text.strip().split('\n'):
            parts = line.split(':')
            name = parts[0].split(' ')[0]
            type_ = re.search(r'(\w+)', parts[0].split(' ')[1]).group(1)
            parameters[name] = {
                "type": type_,
                "description": parts[1]
            }
    else:
        parameters = {}

    # Create the tool definition
    tool_definition = {
        "type": "function",
        "function": {
            "name": function_name,
            "description": description_func,
            "parameters": {
                "type":"object",
                "properties": parameters,
                "required":list(parameters.keys())
            },
        }
    }

    return tool_definition


# Function registry
FUNCTION_REGISTRY: Dict[str, Callable] = {}

def register_function(func: Callable):
    FUNCTION_REGISTRY[func.__name__] = func
    return func

# Sample tool
@register_function
def count_letters(word, letter):
    """
Counts the occurrences of a specified letter in a given word.

Parameters:
word (str): The word to search within.
letter (str): The letter to count.

Returns:
str: A message indicating how many times the letter appears in the word, or an error message if an exception occurs.
"""
    try:
        count = word.lower().count(letter.lower())
        return f"The letter '{letter}' appears {count} times in '{word}'"
    except Exception as e:
        return f"Error counting letters: {str(e)}"

@register_function
def reverse_word(word):
    """
Reverses the characters in a given word.

Parameters:
word (str): The word to be reversed.

Returns:
str: The reversed word.
"""
    return word[::-1]

TOOLS = [docstring_to_tool_definition(func,FUNCTION_REGISTRY) for func in FUNCTION_REGISTRY]