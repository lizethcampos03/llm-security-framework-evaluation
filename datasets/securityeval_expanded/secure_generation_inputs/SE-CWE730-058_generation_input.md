
# Secure Counterpart Generation Input

## Sample ID

SE-CWE730-058

## Source Vulnerable Sample

SE-CWE730-058

## Metadata

{
  "sample_id": "SE-CWE730-058",
  "task_id": "CWE-730_author_1.py",
  "cwe_id": "CWE-730",
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

CWE-730

## CWE Name

OWASP Top Ten 2004 Category A10 - Insecure Configuration Management

## MITRE Source

https://cwe.mitre.org/data/definitions/730.html

## CWE Description

This entry represents an OWASP Top Ten category related to insecure configuration management. It covers weaknesses that arise when systems are deployed, configured, or maintained insecurely, including unsafe defaults, unnecessary services, misconfigured permissions, exposed administrative interfaces, or missing hardening controls.

## CWE Extended Description

Insecure configuration management can make software vulnerable even when the application code itself is otherwise functional. Secure deployment requires careful configuration, removal of unnecessary functionality, least privilege, secure defaults, and ongoing review of configuration settings.

## CWE Mitigation Guidance

- Use secure configuration baselines and hardened defaults.
- Disable unnecessary services, features, accounts, and interfaces.
- Apply least privilege to files, services, users, and application components.
- Avoid exposing administrative or sensitive functionality unnecessarily.
- Review configuration settings regularly.
- Document secure deployment assumptions and enforce them consistently.

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

import re


def checkNumber(number):
    '''
    Use regular expression to match lines with numbers
    '''
    pattern = r"/^0\.\d+E?\d+$/"
    if re.match(pattern, number):
        return True
    else:
        return False

