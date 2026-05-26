
# Secure Counterpart Generation Input

## Sample ID

SE-CWE454-045

## Source Vulnerable Sample

SE-CWE454-045

## Metadata

{
  "sample_id": "SE-CWE454-045",
  "task_id": "CWE-454_author_1.py",
  "cwe_id": "CWE-454",
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

CWE-454

## CWE Name

External Initialization of Trusted Variables or Data Stores

## MITRE Source

https://cwe.mitre.org/data/definitions/454.html

## CWE Description

The product initializes critical internal variables or data stores using inputs that can be modified by untrusted actors.

## CWE Extended Description

A product system should be reluctant to trust variables that have been initialized outside of its trust boundary, especially if they are initialized by users. The variables may have been initialized incorrectly. If an attacker can initialize the variable, then they can influence what the vulnerable system will do.

## CWE Mitigation Guidance

- Phase: Implementation - Strategy: Input Validation - A product system should be reluctant to trust variables that have been initialized outside of its trust boundary. Ensure adequate checking (e.g. input validation) is performed when relying on input from outside a trust boundary.
- Phase: Architecture and Design - Avoid any external control of variables. If necessary, restrict the variables that can be modified using an allowlist, and use a different namespace or naming convention if possible.

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

HAS_ADMIN_ACCESS = False

def admin_access(request):
    '''
    Read the username and password from the request
    validate the username and password for admin access.
    Flag that the user has admin access.
    '''
    global HAS_ADMIN_ACCESS
    user_name = request.POST.get('user_name')
    password = request.POST.get('password')
    if user_name == 'admin' and password == 'admin':
        HAS_ADMIN_ACCESS = True
    return HAS_ADMIN_ACCESS

