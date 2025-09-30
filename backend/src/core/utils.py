def to_camel(string: str) -> str:
    """
    Конверт snake_case в camelCase.
    """
    
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])