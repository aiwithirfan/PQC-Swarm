"""CrewAI task definitions for PQC-Swarm."""
from __future__ import annotations

from crewai import Agent, Task


def build_audit_task(agent: Agent, code: str, language: str) -> Task:
    return Task(
        description=(
            f"Audit the following {language} code for quantum-vulnerable "
            "or cryptographically weak primitives.\n\n"
            f"```{language.lower()}\n{code}\n```\n\n"

            "Produce a Markdown report containing:\n"
            "1. Executive summary and overall risk rating.\n"
            "2. A findings table with columns: Finding | Location | Algorithm | "
            "Quantum Threat | Severity.\n"
            "3. Exact line-level evidence from the supplied code.\n"
            "4. A recommended NIST migration for each finding.\n\n"

            "Important accuracy rules:\n"
            "- RSA, ECC, ECDH, DH and DSA are classical public-key algorithms "
            "and are not post-quantum secure against sufficiently capable "
            "quantum computers.\n"
            "- SHA-1 is classically deprecated because of collision weaknesses. "
            "Do not describe SHA-1 as being broken by Shor's algorithm.\n"
            "- Use current NIST names: ML-KEM (FIPS 203), ML-DSA (FIPS 204), "
            "and SLH-DSA (FIPS 205).\n"
            "- Do not invent vulnerabilities that are not present in the code.\n"
            "- Do not speculate about when quantum computers will break these algorithms."
        ),
        expected_output=(
            "A structured Markdown audit report with an executive summary, "
            "findings table, line-level evidence, severity ratings, and "
            "NIST migration recommendations."
        ),
        agent=agent,
    )


def build_refactor_task(
    agent: Agent,
    context_tasks: list[Task],
    code: str,
    language: str,
) -> Task:
    return Task(
        description=(
            f"Using the audit report, rewrite the original {language} code so "
            "quantum-vulnerable public-key cryptography is migrated to "
            "NIST-standardized post-quantum cryptography.\n\n"

            f"Original code:\n```{language.lower()}\n{code}\n```\n\n"

            "Implementation requirements:\n"
            "1. Use the Python package `pqcrypto`.\n"
            "2. Use `pqcrypto.kem.ml_kem_768` for ML-KEM-768 (NIST FIPS 203).\n"
            "3. Use `pqcrypto.sign.ml_dsa_65` for ML-DSA-65 (NIST FIPS 204).\n"
            "4. ML-DSA-65 IS a valid NIST FIPS 204 parameter set. Do not mark "
            "it as non-compliant merely because the parameter level is 65.\n"
            "5. Do not invent packages such as `mlkem` or `ml_dsa`.\n"
            "6. Do not invent APIs such as `generate_keypair()`, `encapsulate()`, "
            "or `decapsulate()`.\n"
            "7. Use the documented `pqcrypto` operations such as `keygen()`, "
            "`encaps()`, `decaps()`, `sign()`, and `verify()` where applicable.\n"
            "8. ML-KEM establishes a shared secret; it does NOT directly encrypt "
            "an arbitrary plaintext session key.\n"
            "9. If the original function accepts an externally supplied "
            "`session_key`, use ML-KEM to establish a shared secret and "
            "AES-256-GCM to actually encrypt that supplied session key.\n"
            "10. The decrypt function must reverse that process and recover "
            "the original supplied session key.\n"
            "11. Preserve the original function names and behavior as closely "
            "as reasonably possible.\n"
            "12. Preserve signing functionality with ML-DSA.\n"
            "13. Include a signature verification function when needed to "
            "provide complete signing/verification functionality.\n"
            "14. Use secure nonce generation for AES-GCM.\n"
            "15. Do not use RSA, ECC, ECDH, DH, DSA, or SHA-1 in the refactored code.\n"
            "16. Add short comments explaining the cryptographic migration.\n"
            "17. Put required pip packages in a comment at the top.\n"
            "18. Return ONE complete Python code block followed by a short "
            "bullet list of changes.\n"
            "19. Never leave a function, string, parenthesis, import, or code "
            "block incomplete.\n"
            "20. If an API cannot be confidently established, explicitly flag "
            "it for verification instead of inventing an API."
        ),
        expected_output=(
            "One complete Python implementation using documented pqcrypto "
            "APIs, followed by a concise change summary."
        ),
        agent=agent,
        context=context_tasks,
    )


def build_verify_task(
    agent: Agent,
    context_tasks: list[Task],
    language: str,
) -> Task:
    return Task(
        description=(
            f"Strictly verify the COMPLETE refactored {language} code from "
            "the previous Refactorer task.\n\n"

            "You MUST inspect both the audit report and the complete "
            "refactored code before giving your verdict.\n\n"

            "Verification requirements:\n"
            "1. Check Python syntax and code completeness.\n"
            "2. Check every import and referenced function.\n"
            "3. Verify that the pqcrypto APIs used are consistent with "
            "the specified dependency.\n"
            "4. Check ML-KEM key generation, encapsulation and decapsulation.\n"
            "5. Check ML-DSA key generation, signing and verification.\n"
            "6. Check AES-256-GCM key length, nonce handling, encryption "
            "and decryption.\n"
            "7. Check that an externally supplied session_key is actually "
            "encrypted and recovered, rather than being silently ignored.\n"
            "8. Check that RSA, ECC, ECDH, DH, DSA and SHA-1 have been removed.\n"
            "9. Check NIST terminology: ML-KEM FIPS 203, ML-DSA FIPS 204, "
            "SLH-DSA FIPS 205.\n"
            "10. ML-DSA-65 is a valid FIPS 204 parameter set. Do NOT report "
            "`ml_dsa_65` as non-compliant merely because it is the 65 parameter set.\n"
            "11. Check for missing signature verification functionality.\n"
            "12. Check key management and serialization requirements.\n"
            "13. Check error handling and input validation.\n"
            "14. Do not assume an AI-generated API is valid merely because "
            "the code looks syntactically correct.\n"
            "15. If an external package/API requires confirmation, mark it "
            "as a warning instead of silently approving it.\n\n"

            "Your response MUST begin with exactly ONE of these lines:\n"
            "VERDICT: PASS\n"
            "VERDICT: PASS WITH WARNINGS\n"
            "VERDICT: FAIL\n\n"

            "After the verdict provide:\n"
            "- Verification checklist\n"
            "- Issues found\n"
            "- Suggested fixes\n"
            "- Readiness summary\n\n"

            "IMPORTANT: Always return a non-empty verification report. "
            "Never return an empty response."
        ),
        expected_output=(
            "A non-empty Markdown verification report beginning with exactly "
            "'VERDICT: PASS', 'VERDICT: PASS WITH WARNINGS', or "
            "'VERDICT: FAIL'."
        ),
        agent=agent,
        context=context_tasks,
    )
