import logging
import re


def inputConversion():
    '''
    Take a string input from the user,
    convert it to an integer within a try-except block,
    and log a conversion error if a ValueError occurs.
    Return the converted user input.
    '''
    user_input = input("Enter a number: ")

    try:
        return int(user_input)

    except ValueError:
        sanitized_input = re.sub(r'[\r\n]', '', user_input)

        logging.error(
            "The input was not a number: %s",
            sanitized_input
        )

        return None