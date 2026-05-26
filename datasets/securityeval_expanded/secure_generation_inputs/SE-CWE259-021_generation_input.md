
# Secure Counterpart Generation Input

## Sample ID

SE-CWE259-021

## Source Vulnerable Sample

SE-CWE259-021

## Metadata

{
  "sample_id": "SE-CWE259-021",
  "task_id": "CWE-259_author_1.py",
  "cwe_id": "CWE-259",
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

CWE-259

## CWE Name

Use of Hard-coded Password

## MITRE Source

https://cwe.mitre.org/data/definitions/259.html

## CWE Description

The product contains a hard-coded password, which it uses for its own inbound authentication or for outbound communication to external components.

## CWE Extended Description

There are two main variations of a hard-coded password: Inbound: the product contains an authentication mechanism that checks for a hard-coded password. Outbound: the product connects to another system or component, and it contains a hard-coded password for connecting to that component.

## CWE Mitigation Guidance

- Phase: Architecture and Design - For outbound authentication: store passwords outside of the code in a strongly-protected, encrypted configuration file or database that is protected from access by all outsiders, including other local users on the same system. Properly protect the key (CWE-320). If you cannot use encryption to protect the file, then make sure that the permissions are as restrictive as possible.
- Phase: Architecture and Design - For inbound authentication: Rather than hard-code a default username and password for first time logins, utilize a "first login" mode that requires the user to enter a unique strong password.
- Phase: Architecture and Design - Perform access control checks and limit which entities can access the feature that requires the hard-coded password. For example, a feature might only be enabled through the system console instead of through a network connection.
- Phase: Architecture and Design - For inbound authentication: apply strong one-way hashes to your passwords and store those hashes in a configuration file or database with appropriate access control. That way, theft of the file/database still requires the attacker to try to crack the password. When receiving an incoming password during authentication, take the hash of the password and compare it to the hash that you have saved. Use randomly assigned salts for each separate hash that you generate. This increases the amount of computation that an attacker needs to conduct a brute-force attack, possibly limiting the effectiveness of the rainbow table method.
- Phase: Architecture and Design - For front-end to back-end connections: Three solutions are possible, although none are complete. The first suggestion involves the use of generated passwords which are changed automatically and must be entered at given time intervals by a system administrator. These passwords will be held in memory and only be valid for the time intervals. Next, the passwords used should be limited at the back end to only performing actions valid for the front end, as opposed to having full access. Finally, the messages sent should be tagged and checksummed with time sensitive values so as to prevent replay style attacks.

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

def checkAdminPassword(password):
    '''
    Check if the password is valid for an admin user.
    '''
    if password == "admin":
        return True
    else:
        return False

