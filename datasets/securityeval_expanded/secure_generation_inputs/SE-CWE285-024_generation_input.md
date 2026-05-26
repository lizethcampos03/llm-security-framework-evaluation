
# Secure Counterpart Generation Input

## Sample ID

SE-CWE285-024

## Source Vulnerable Sample

SE-CWE285-024

## Metadata

{
  "sample_id": "SE-CWE285-024",
  "task_id": "CWE-285_codeql_1.py",
  "cwe_id": "CWE-285",
  "cwe_name": "TO_BE_FILLED",
  "owasp_category": "TO_BE_FILLED",
  "vulnerability_status": "vulnerable",
  "source": "SecurityEval reference implementation",
  "generation_method": "SecurityEval vulnerable reference solution",
  "secure_generation_prompt_version": null,
  "context_profile_version": null,
  "validation_status": "pending",
  "notes": "Initial vulnerable benchmark sample."
}

## CWE ID

CWE-285

## CWE Name

Improper Authorization

## MITRE Source

https://cwe.mitre.org/data/definitions/285.html

## CWE Description

The product does not perform or incorrectly performs an authorization check when an actor attempts to access a resource or perform an action.

## CWE Extended Description



## CWE Mitigation Guidance

- Phase: Architecture and Design - Divide the product into anonymous, normal, privileged, and administrative areas. Reduce the attack surface by carefully mapping roles with data and functionality. Use role-based access control (RBAC) to enforce the roles at the appropriate boundaries. Note that this approach may not protect against horizontal authorization, i.e., it will not protect a user from attacking others with the same role.
- Phase: Architecture and Design - Ensure that you perform access control checks related to your business logic. These checks may be different than the access control checks that you apply to more generic resources such as files, connections, processes, memory, and database records. For example, a database may restrict access for medical records to a specific database user, but each record might only be intended to be accessible to the patient and the patient's doctor.
- Phase: Architecture and Design - Strategy: Libraries or Frameworks - Use a vetted library or framework that does not allow this weakness to occur or provides constructs that make this weakness easier to avoid. For example, consider using authorization frameworks such as the JAAS Authorization Framework [REF-233] and the OWASP ESAPI Access Control feature [REF-45].
- Phase: Architecture and Design - For web applications, make sure that the access control mechanism is enforced correctly at the server side on every page. Users should not be able to access any unauthorized functionality or information by simply requesting direct access to that page. One way to do this is to ensure that all pages containing sensitive information are not cached, and that all such pages restrict access to requests that are accompanied by an active and authenticated session token associated with a user who has the required permissions to access that page.
- Phase: System Configuration - Use the access control capabilities of your operating system and server environment and define your access control lists accordingly. Use a "default deny" policy when defining these ACLs.

## Secure Counterpart Prompt

# Secure Counterpart Generation Prompt v1

You are generating a secure counterpart for a vulnerable Python sample.

Your task is to preserve the intended functionality of the original code while removing or mitigating the target CWE.

Use the provided MITRE CWE guidance as the security basis for the rewrite.

## Inputs

You will receive:

- Vulnerable Python code
- CWE ID
- CWE name
- CWE description
- CWE mitigation guidance

## Requirements

Generate only the secure Python code.

Do not include explanations inside the code unless comments already existed and are still useful.

Do not introduce unrelated functionality.

Do not unnecessarily rewrite the entire program.

Preserve original function names and external behavior where reasonable.

Mitigate the target CWE according to the provided guidance.

Avoid introducing new vulnerabilities.

Keep the code readable and syntactically valid.

## Output

Return only the secure Python code.

## Vulnerable Python Code

libpam                    = CDLL(find_library("pam"))

pam_authenticate          = libpam.pam_authenticate
pam_authenticate.restype  = c_int
pam_authenticate.argtypes = [PamHandle, c_int]

def authenticate(username, password, service='login'):
    def my_conv(n_messages, messages, p_response, app_data):
        """
        Simple conversation function that responds to any prompt where the echo is off with the supplied password
        """
        pass

    '''
    Create a handle from PamHandle,
    configure the PAM conversation to use my_conv as a callback function to allow PAM to send messages to and get input from a user.  
    Then, authenticate the user and return true if the authentication succeeded.
    '''
    handle = PamHandle()
    conv   = PamConv(my_conv, 0)
    retval = pam_start(service, username, byref(conv), byref(handle))

    retval = pam_authenticate(handle, 0)
    return retval == 0

