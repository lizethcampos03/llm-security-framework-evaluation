import subprocess
import shlex

def executeCommand():
    '''
    Read a command from a user input, validate it, and execute it
    '''
    user_input = input("Enter a command: ")
    
    # Allowlist of permitted commands
    allowed_commands = {
        'ls': ['ls'],
        'pwd': ['pwd'],
        'date': ['date'],
        'whoami': ['whoami']
    }
    
    # Parse and validate input
    try:
        tokens = shlex.split(user_input)
    except ValueError:
        print("Invalid command format")
        return
    
    if not tokens:
        print("No command provided")
        return
    
    command_name = tokens[0]
    
    # Check if command is in allowlist
    if command_name not in allowed_commands:
        print(f"Command '{command_name}' is not allowed")
        return
    
    # Execute command without shell, using array of arguments
    try:
        subprocess.call(tokens, shell=False)
    except (subprocess.SubprocessError, OSError) as e:
        print("Command execution failed")