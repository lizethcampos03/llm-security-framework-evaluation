import logging
import re


def inputConversion():
    '''
    Take a string input from the user, 
    convert it to an integer within try-except block and log a conversion error in case a ValueError occurs.
    Return the converted user input.
    '''
    try:
        userInput = input("Enter a number: ")
        userInput = int(userInput)
    except ValueError:
        sanitized_input = re.sub(r'[\r\n]', '', userInput)
        logging.error("The input was not a number: %s", sanitized_input)
    return userInput