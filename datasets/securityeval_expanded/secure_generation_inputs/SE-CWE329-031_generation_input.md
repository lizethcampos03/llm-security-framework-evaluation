
# Secure Counterpart Generation Input

## Sample ID

SE-CWE329-031

## Source Vulnerable Sample

SE-CWE329-031

## Metadata

{
  "sample_id": "SE-CWE329-031",
  "task_id": "CWE-329_sonar_1.py",
  "cwe_id": "CWE-329",
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

CWE-329

## CWE Name

Generation of Predictable IV with CBC Mode

## MITRE Source

https://cwe.mitre.org/data/definitions/329.html

## CWE Description

The product generates and uses a predictable initialization Vector (IV) with Cipher Block Chaining (CBC) Mode, which causes algorithms to be susceptible to dictionary attacks when they are encrypted under the same key.

## CWE Extended Description

CBC mode eliminates a weakness of Electronic Code Book (ECB) mode by allowing identical plaintext blocks to be encrypted to different ciphertext blocks. This is possible by the XOR-ing of an IV with the initial plaintext block so that every plaintext block in the chain is XOR'd with a different value before encryption. If IVs are reused, then identical plaintexts would be encrypted to identical ciphertexts. However, even if IVs are not identical but are predictable, then they still break the security of CBC mode against Chosen Plaintext Attacks (CPA).

## CWE Mitigation Guidance

- Phase: Implementation - NIST recommends two methods of generating unpredictable IVs for CBC mode [REF-1172]. The first is to generate the IV randomly. The second method is to encrypt a nonce with the same key and cipher to be used to encrypt the plaintext. In this case the nonce must be unique but can be predictable, since the block cipher will act as a pseudo random permutation.

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

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def getEncryptionKey(key):
    '''
    Create a Cipher using AES and CBC mode.
    Then, encrypt the key using this cipher and return it.
    '''
    static_vector = b'x' * 16
    cipher = Cipher(algorithms.AES(key), modes.CBC(static_vector))
    cipher.encryptor()

