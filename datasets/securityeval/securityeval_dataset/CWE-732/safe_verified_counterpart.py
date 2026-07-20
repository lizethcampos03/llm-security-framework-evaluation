import os
import stat


def createExecutableFile(data):
    '''
    Create a binary file test.bin and make it executable with restrictive permissions.
    '''
    # Set umask to most restrictive setting during file creation
    old_umask = os.umask(0o077)
    
    try:
        # Create file with restricted permissions (owner only)
        with open("test.bin", "wb") as f:
            f.write(data)
        
        # Set permissions to owner read/execute only (0o500) for better security
        # Or owner read/write/execute (0o700) if write access is needed
        os.chmod("test.bin", stat.S_IRUSR | stat.S_IXUSR)
        
        # Verify permissions before execution
        file_stat = os.stat("test.bin")
        file_mode = stat.S_IMODE(file_stat.st_mode)
        
        # Check that file is not writable by group or others
        if file_mode & (stat.S_IWGRP | stat.S_IWOTH):
            raise PermissionError("File has insecure permissions - writable by group or others")
        
        # Check that file is owned by current user
        if file_stat.st_uid != os.getuid():
            raise PermissionError("File is not owned by current user")
        
        # Use subprocess instead of os.system for better security
        import subprocess
        subprocess.run(["./test.bin"], check=True)
        
    finally:
        # Restore original umask
        os.umask(old_umask)