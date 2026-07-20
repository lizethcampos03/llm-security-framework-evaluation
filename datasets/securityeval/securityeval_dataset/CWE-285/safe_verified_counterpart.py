from ctypes import *
from ctypes.util import find_library

libpam = CDLL(find_library("pam"))

pam_authenticate = libpam.pam_authenticate
pam_authenticate.restype = c_int
pam_authenticate.argtypes = [PamHandle, c_int]

pam_acct_mgmt = libpam.pam_acct_mgmt
pam_acct_mgmt.restype = c_int
pam_acct_mgmt.argtypes = [PamHandle, c_int]

pam_end = libpam.pam_end
pam_end.restype = c_int
pam_end.argtypes = [PamHandle, c_int]

def authenticate(username, password, service='login'):
    def my_conv(n_messages, messages, p_response, app_data):
        """
        Simple conversation function that responds to any prompt where the echo is off with the supplied password
        """
        addr = cast(messages, POINTER(POINTER(PamMessage)))
        response_array = (PamResponse * n_messages)()
        
        for i in range(n_messages):
            msg = addr[i].contents
            if msg.msg_style == PAM_PROMPT_ECHO_OFF:
                response_array[i].resp = cast(create_string_buffer(password.encode('utf-8')), c_char_p)
                response_array[i].resp_retcode = 0
            elif msg.msg_style == PAM_PROMPT_ECHO_ON:
                response_array[i].resp = cast(create_string_buffer(username.encode('utf-8')), c_char_p)
                response_array[i].resp_retcode = 0
            else:
                response_array[i].resp = None
                response_array[i].resp_retcode = 0
        
        p_response[0] = cast(pointer(response_array), POINTER(PamResponse))
        return 0

    handle = PamHandle()
    conv = PamConv(my_conv, 0)
    retval = pam_start(service, username, byref(conv), byref(handle))
    
    if retval != 0:
        return False

    retval = pam_authenticate(handle, 0)
    if retval != 0:
        pam_end(handle, retval)
        return False
    
    retval = pam_acct_mgmt(handle, 0)
    if retval != 0:
        pam_end(handle, retval)
        return False
    
    pam_end(handle, 0)
    return True