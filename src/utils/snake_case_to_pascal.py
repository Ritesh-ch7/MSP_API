def snake_to_pascal(snake_str):
    """
    Converts a snake_case string to PascalCase.

    Args:
    - snake_str (str): The snake_case string to be converted.

    Returns:
    str: The PascalCase version of the input string.
    """
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)