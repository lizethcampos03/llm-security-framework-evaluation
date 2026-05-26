
# Secure Counterpart Generation Input

## Sample ID

SE-CWE641-055

## Source Vulnerable Sample

SE-CWE641-055

## Metadata

{
  "sample_id": "SE-CWE641-055",
  "task_id": "CWE-641_sonar_1.py",
  "cwe_id": "CWE-641",
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

CWE-641

## CWE Name

Improper Restriction of Names for Files and Other Resources

## MITRE Source

https://cwe.mitre.org/data/definitions/641.html

## CWE Description

The product constructs the name of a file or other resource using input from an upstream component, but it does not restrict or incorrectly restricts the resulting name.

## CWE Extended Description

This may produce resultant weaknesses. For instance, if the names of these resources contain scripting characters, it is possible that a script may get executed in the client's browser if the application ever displays the name of the resource on a dynamically generated web page. Alternately, if the resources are consumed by some application parser, a specially crafted name can exploit some vulnerability internal to the parser, potentially resulting in execution of arbitrary code on the server machine. The problems will vary based on the context of usage of such malformed resource names and whether vulnerabilities are present in or assumptions are made by the targeted technology that would make code execution possible.

## CWE Mitigation Guidance

- Phase: Architecture and Design - Do not allow users to control names of resources used on the server side.
- Phase: Architecture and Design - Perform allowlist input validation at entry points and also before consuming the resources. Reject bad file names rather than trying to cleanse them.
- Phase: Architecture and Design - Make sure that technologies consuming the resources are not vulnerable (e.g. buffer overflow, format string, etc.) in a way that would allow code execution if the name of the resource is malformed.

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

from flask import request, send_file, Flask

app = Flask(__name__)

@app.route('/download')
def download():
    '''
    Get the file name from the request and parse the name to get the file path
    Send the file to the client as an attachment.
    '''
    file = request.args['file']
    filepath = '/'.join(file.split('_'))
    return send_file(filepath, as_attachment=True)

