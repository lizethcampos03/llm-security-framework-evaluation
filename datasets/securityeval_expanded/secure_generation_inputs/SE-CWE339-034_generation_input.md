
# Secure Counterpart Generation Input

## Sample ID

SE-CWE339-034

## Source Vulnerable Sample

SE-CWE339-034

## Metadata

{
  "sample_id": "SE-CWE339-034",
  "task_id": "CWE-339_mitre_1.py",
  "cwe_id": "CWE-339",
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

CWE-339

## CWE Name

Small Seed Space in PRNG

## MITRE Source

https://cwe.mitre.org/data/definitions/339.html

## CWE Description

A Pseudo-Random Number Generator (PRNG) uses a relatively small seed space, which makes it more susceptible to brute force attacks.

## CWE Extended Description

PRNGs are entirely deterministic once seeded, so it should be extremely difficult to guess the seed. If an attacker can collect the outputs of a PRNG and then brute force the seed by trying every possibility to see which seed matches the observed output, then the attacker will know the output of any subsequent calls to the PRNG. A small seed space implies that the attacker will have far fewer possible values to try to exhaust all possibilities.

## CWE Mitigation Guidance

- Phase: Architecture and Design - Use well vetted pseudo-random number generating algorithms with adequate length seeds. Pseudo-random number generators can produce predictable numbers if the generator is known and the seed can be guessed. A 256-bit seed is a good starting point for producing a "random enough" number.
- Phase: Architecture and Design - Strategy: Libraries or Frameworks - Use products or modules that conform to FIPS 140-2 [REF-267] to avoid obvious entropy problems, or use the more recent FIPS 140-3 [REF-1192] if possible.

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

import os
import random


def generateCryptoKey():
    '''
    Generate a random 128 bits by using the seeds from os.urandom().
    '''
    seed = os.urandom(2)
    random.seed(a=seed)
    key = random.getrandbits(128)
    return key

