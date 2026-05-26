
# Secure Counterpart Generation Input

## Sample ID

SE-CWE347-035

## Source Vulnerable Sample

SE-CWE347-035

## Metadata

{
  "sample_id": "SE-CWE347-035",
  "task_id": "CWE-347_sonar_1.py",
  "cwe_id": "CWE-347",
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

CWE-347

## CWE Name

Improper Verification of Cryptographic Signature

## MITRE Source

https://cwe.mitre.org/data/definitions/347.html

## CWE Description

The product does not verify, or incorrectly verifies, the cryptographic signature for data.

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

import jwt


def verifyJsonWebToken(token):
    '''
    Decode the JSON web token passed and return it.
    '''
    return jwt.decode(token, verify=False)

