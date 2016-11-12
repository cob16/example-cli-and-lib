# helper functions
def isMessageBody(line: str) -> bool:
    """
    Returns True if line has more than just whitepsace and unempty or is a comment (contains #)
    """
    return not ( line.isspace() and line.lstrip().startswith('#') )