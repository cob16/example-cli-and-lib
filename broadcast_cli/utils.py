# helper functions
def isMessageBody(line: str) -> bool:
    """
    Returns True if line is unempty or is a comment (contains #)
    """
    line = line.lstrip()
    return line or (not line.startswith('#'))
