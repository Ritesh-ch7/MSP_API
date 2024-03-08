def snake_to_pascal(snake_str):

    """     
    Converts a string in snake_case to PascalCase.   

    Parameters:     
    - snake_str (str): Input string in snake_case.

    Returns:     
    - str: Output string in PascalCase.     
    """

    components = snake_str.split('_')
    return ''.join(x.title() for x in components)