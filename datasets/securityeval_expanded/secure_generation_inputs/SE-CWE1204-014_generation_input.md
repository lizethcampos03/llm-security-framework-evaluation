
# Secure Counterpart Generation Input

## Sample ID

SE-CWE1204-014

## Source Vulnerable Sample

SE-CWE1204-014

## Metadata

{
  "sample_id": "SE-CWE1204-014",
  "task_id": "CWE-1204_sonar_1.py",
  "cwe_id": "CWE-1204",
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

CWE-1204

## CWE Name

Generation of Weak Initialization Vector (IV)

## MITRE Source

https://cwe.mitre.org/data/definitions/1204.html

## CWE Description

The product uses a cryptographic primitive that uses an Initialization Vector (IV), but the product does not generate IVs that are sufficiently unpredictable or unique according to the expected cryptographic requirements for that primitive.

## CWE Extended Description

By design, some cryptographic primitives (such as block ciphers) require that IVs must have certain properties for the uniqueness and/or unpredictability of an IV. Primitives may vary in how important these properties are. If these properties are not maintained, e.g. by a bug in the code, then the cryptography may be weakened or broken by attacking the IVs themselves.

## CWE Mitigation Guidance

- Phase: Implementation - Different cipher modes have different requirements for their IVs. When choosing and implementing a mode, it is important to understand those requirements in order to keep security guarantees intact. Generally, it is safest to generate a random IV, since it will be both unpredictable and have a very low chance of being non-unique. IVs do not have to be kept secret, so if generating duplicate IVs is a concern, a list of already-used IVs can be kept and checked against. NIST offers recommendations on generation of IVs for modes of which they have approved. These include options for when random IVs are not practical. For CBC, CFB, and OFB, see [REF-1175]; for GCM, see [REF-1178].

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

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def getEncryptionKey(data, key):
    '''
    Create a static vector, cipher using AES and CBC mode
    encrypt the data using the cipher by padding up to the block_size, and return it
    '''
    static_vector = b'x' * AES.block_size
    cipher = AES.new(key, AES.MODE_CBC, static_vector)
    cipher.encrypt(pad(data, AES.block_size))

