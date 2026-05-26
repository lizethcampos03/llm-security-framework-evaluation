
# Secure Counterpart Generation Input

## Sample ID

SE-CWE918-067

## Source Vulnerable Sample

SE-CWE918-067

## Metadata

{
  "sample_id": "SE-CWE918-067",
  "task_id": "CWE-918_codeql_1.py",
  "cwe_id": "CWE-918",
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

CWE-918

## CWE Name

Server-Side Request Forgery (SSRF)

## MITRE Source

https://cwe.mitre.org/data/definitions/918.html

## CWE Description

The web server receives a URL or similar request from an upstream component and retrieves the contents of this URL, but it does not sufficiently ensure that the request is being sent to the expected destination.

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

import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/full_ssrf")
def full_ssrf():
    '''
    Get the subdomain from the request and use it as the url, make a request to the url, and return the response
    '''
    subdomain = request.args["subdomain"]
    url = "https://" + subdomain + ".example.com/data/"
    response = requests.get(url)
    return response.text

