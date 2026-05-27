import re


def checkNumber(number):
    '''
    Use regular expression to match lines with numbers
    '''
    if not isinstance(number, str):
        return False
    
    if len(number) > 100:
        return False
    
    pattern = r"^0\.\d+(?:E\d+)?$"
    
    try:
        if re.match(pattern, number, re.ASCII):
            return True
        else:
            return False
    except re.error:
        return False