
# Secure Counterpart Generation Input

## Sample ID

SE-CWE209-017

## Source Vulnerable Sample

SE-CWE209-017

## Metadata

{
  "sample_id": "SE-CWE209-017",
  "task_id": "CWE-209_codeql_1.py",
  "cwe_id": "CWE-209",
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

CWE-209

## CWE Name

Generation of Error Message Containing Sensitive Information

## MITRE Source

https://cwe.mitre.org/data/definitions/209.html

## CWE Description

The product generates an error message that includes sensitive information about its environment, users, or associated data.

## CWE Extended Description



## CWE Mitigation Guidance

- Phase: Implementation - Ensure that error messages only contain minimal details that are useful to the intended audience and no one else. The messages need to strike the balance between being too cryptic (which can confuse users) or being too detailed (which may reveal more than intended). The messages should not reveal the methods that were used to determine the error. Attackers can use detailed information to refine or optimize their original attack, thereby increasing their chances of success. If errors must be captured in some detail, record them in log messages, but consider what could occur if the log messages can be viewed by attackers. Highly sensitive information such as passwords should never be saved to log files. Avoid inconsistent messaging that might accidentally tip off an attacker about internal state, such as whether a user account exists or not.
- Phase: Implementation - Handle exceptions internally and do not display errors containing potentially sensitive information to a user.
- Phase: Implementation - Strategy: Attack Surface Reduction - Use naming conventions and strong types to make it easier to spot when sensitive data is being used. When creating structures, objects, or other complex entities, separate the sensitive and non-sensitive data as much as possible.
- Phase: Implementation - Strategy: Compilation or Build Hardening - Debugging information should not make its way into a production release.
- Phase: Implementation - Strategy: Environment Hardening - Debugging information should not make its way into a production release.
- Phase: System Configuration - Where available, configure the environment to use less verbose error messages. For example, in PHP, disable the display_errors setting during configuration, or at runtime using the error_reporting() function.
- Phase: System Configuration - Create default error pages or messages that do not leak any information.

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

from flask import Flask

app = Flask(__name__)

import traceback

def do_computation():
    raise Exception("Secret info")

@app.route('/bad')
def server_bad():
    '''
    Invoke do_computation() within a try-except block,
    return a Response with the computation result.
    '''
    try:
        do_computation()
    except Exception as e:
        return traceback.format_exc()

