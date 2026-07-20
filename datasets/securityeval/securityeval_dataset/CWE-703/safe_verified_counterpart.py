def convert_to_int():
    '''
    Take an input from the user (console) and convert it to int within a try-except block.
    '''
    try:
        user_input = input("Enter a number: ")
        return int(user_input)
    except ValueError as e:
        print(f"Error: Invalid input. Please enter a valid integer. ({e})")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None