
# Secure Counterpart Generation Input

## Sample ID

SE-CWE835-065

## Source Vulnerable Sample

SE-CWE835-065

## Metadata

{
  "sample_id": "SE-CWE835-065",
  "task_id": "CWE-835_author_1.py",
  "cwe_id": "CWE-835",
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

CWE-835

## CWE Name

Loop with Unreachable Exit Condition ('Infinite Loop')

## MITRE Source

https://cwe.mitre.org/data/definitions/835.html

## CWE Description

The product contains an iteration or loop with an exit condition that cannot be reached, i.e., an infinite loop.

## CWE Extended Description



## CWE Mitigation Guidance



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

def getFibonacci(n):
    '''
    Compute the n-th fibonacci number using loops only.
    '''
    a, b = 1, 1
    i = 2
    while i < n:
        a, b = b, a + b
    return b

