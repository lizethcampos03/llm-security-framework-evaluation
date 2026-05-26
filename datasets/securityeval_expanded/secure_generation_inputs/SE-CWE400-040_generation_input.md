
# Secure Counterpart Generation Input

## Sample ID

SE-CWE400-040

## Source Vulnerable Sample

SE-CWE400-040

## Metadata

{
  "sample_id": "SE-CWE400-040",
  "task_id": "CWE-400_sonar_1.py",
  "cwe_id": "CWE-400",
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

CWE-400

## CWE Name

Uncontrolled Resource Consumption

## MITRE Source

https://cwe.mitre.org/data/definitions/400.html

## CWE Description

The product does not properly control the allocation and maintenance of a limited resource.

## CWE Extended Description



## CWE Mitigation Guidance

- Phase: Architecture and Design - Design throttling mechanisms into the system architecture. The best protection is to limit the amount of resources that an unauthorized user can cause to be expended. A strong authentication and access control model will help prevent such attacks from occurring in the first place. The login application should be protected against DoS attacks as much as possible. Limiting the database access, perhaps by caching result sets, can help minimize the resources expended. To further limit the potential for a DoS attack, consider tracking the rate of requests received from users and blocking requests that exceed a defined rate threshold.
- Phase: Architecture and Design - Mitigation of resource exhaustion attacks requires that the target system either: recognizes the attack and denies that user further access for a given amount of time, or uniformly throttles all requests in order to make it more difficult to consume resources more quickly than they can again be freed. The first of these solutions is an issue in itself though, since it may allow attackers to prevent the use of the system by a particular valid user. If the attacker impersonates the valid user, they may be able to prevent the user from accessing the server in question. The second solution is simply difficult to effectively institute -- and even when properly done, it does not provide a full solution. It simply makes the attack require more resources on the part of the attacker.
- Phase: Architecture and Design - Ensure that protocols have specific limits of scale placed on them.
- Phase: Implementation - Ensure that all failures in resource allocation place the system into a safe posture.

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

from flask import request, Flask

app = Flask(__name__)


@app.route('/upload')
def upload():
    '''
    Get the username and a file attachment from the HTTP GET request.
    Then, search the username in the filename of the attachment.
    '''

    username = request.args.get('username')
    filename = request.files.get('attachment').filename

    re.search(username, filename)

