import os
import signal
import pwd


def killProcess(processID):
    '''
    Kill the process with the given processID.
    '''
    try:
        # Verify ownership before killing the process
        current_uid = os.getuid()
        
        # Get the owner UID of the target process
        proc_status_path = f'/proc/{processID}/status'
        
        if not os.path.exists(proc_status_path):
            raise ValueError(f"Process {processID} does not exist")
        
        with open(proc_status_path, 'r') as f:
            for line in f:
                if line.startswith('Uid:'):
                    # The format is "Uid: real effective saved fs"
                    proc_uid = int(line.split()[1])
                    break
            else:
                raise ValueError(f"Could not determine owner of process {processID}")
        
        # Only allow killing if current user owns the process
        # (unless running as root, which has uid 0)
        if current_uid != 0 and current_uid != proc_uid:
            raise PermissionError(
                f"Cannot kill process {processID}: not owned by current user"
            )
        
        os.kill(processID, signal.SIGKILL)
        
    except (OSError, IOError, ValueError, PermissionError) as e:
        raise RuntimeError(f"Failed to kill process {processID}: {e}")