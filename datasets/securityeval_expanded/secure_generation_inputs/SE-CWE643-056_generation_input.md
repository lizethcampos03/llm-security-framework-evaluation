
# Secure Counterpart Generation Input

## Sample ID

SE-CWE643-056

## Source Vulnerable Sample

SE-CWE643-056

## Metadata

{
  "sample_id": "SE-CWE643-056",
  "task_id": "CWE-643_codeql_1.py",
  "cwe_id": "CWE-643",
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

CWE-643

## CWE Name

Improper Neutralization of Data within XPath Expressions ('XPath Injection')

## MITRE Source

https://cwe.mitre.org/data/definitions/643.html

## CWE Description

The product uses external input to dynamically construct an XPath expression used to retrieve data from an XML database, but it does not neutralize or incorrectly neutralizes that input. This allows an attacker to control the structure of the query.

## CWE Extended Description

The net effect is that the attacker will have control over the information selected from the XML database and may use that ability to control application flow, modify logic, retrieve unauthorized data, or bypass important checks (e.g. authentication).

## CWE Mitigation Guidance

- Phase: Implementation - Use parameterized XPath queries (e.g. using XQuery). This will help ensure separation between data plane and control plane.
- Phase: Implementation - Properly validate user input. Reject data where appropriate, filter where appropriate and escape where appropriate. Make sure input that will be used in XPath queries is safe in that context.

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

from lxml import etree
from io import StringIO

from django.http import HttpResponse


def xpath_query(request):
    '''
    Get the `xpath` value from the GET request,
    get the 'xml' value from the GET request,
    construct and parse the xml payload,
    return the result of the XPath query "/tag[@id={}]" format from the parsed xml
    '''
    value = request.GET['xpath']
    f = StringIO(request.GET['xml'])
    tree = etree.parse(f)
    return tree.xpath("/tag[@id='%s']" % value)

