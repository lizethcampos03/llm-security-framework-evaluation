
# Secure Counterpart Generation Input

## Sample ID

SE-CWE827-064

## Source Vulnerable Sample

SE-CWE827-064

## Metadata

{
  "sample_id": "SE-CWE827-064",
  "task_id": "CWE-827_sonar_1.py",
  "cwe_id": "CWE-827",
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

CWE-827

## CWE Name

Improper Control of Document Type Definition

## MITRE Source

https://cwe.mitre.org/data/definitions/827.html

## CWE Description

The product does not restrict a reference to a Document Type Definition (DTD) to the intended control sphere. This might allow attackers to reference arbitrary DTDs, possibly causing the product to expose files, consume excessive system resources, or execute arbitrary http requests on behalf of the attacker.

## CWE Extended Description

As DTDs are processed, they might try to read or include files on the machine performing the parsing. If an attacker is able to control the DTD, then the attacker might be able to specify sensitive resources or requests or provide malicious content. For example, the SOAP specification prohibits SOAP messages from containing DTDs.

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

from lxml import etree


def getXmlRoot():
    '''
    Create an XML parser and parse the resources/c.xml file and return the root element
    '''
    parser = etree.XMLParser()
    tree = etree.parse('resources/c.xml', parser)
    root = tree.getroot()
    return root

