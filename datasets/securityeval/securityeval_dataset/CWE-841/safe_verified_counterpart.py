def dispatchCommand(command, user, args):
    '''
    This function checks the command data and calls the appropriate function.
    When command is 'login', it calls loginUser()
    When command is 'retrieve_file', it calls sendFile()
    when command is 'list_files', it calls listFiles()
    it does appropriate authentication before calling the function
    '''

    if command == 'login':
        loginUser(args)
        return
    if command == 'retrieve_file':
        if authenticated(user) and ownsFile(user, args):
            sendFile(args)
            return
        else:
            raise PermissionError("User not authenticated or does not own file")
    if command == 'list_files':
        if authenticated(user):
            listFiles(args)
            return
        else:
            raise PermissionError("User not authenticated")
    
    raise ValueError("Invalid command")