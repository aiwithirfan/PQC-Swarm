"""CrewAI agent definitions for PQC-Swarm."""
from __future__ import annotations

from crewai import Agent, BaseLLM


def build_auditor(llm: BaseLLM) -> Agent:
    return Agent(
        role="Quantum Vulnerability Auditor",
        goal=(
            "Analyze the provided source code and identify every cryptographic "
            "primitive that is vulnerable to quantum attacks or is otherwise "
            "cryptographically weak. Focus on RSA, ECC/ECDSA/ECDH, DH, DSA, "
            "weak hashes, weak key sizes, and insecure cryptographic constructions. "
            "Provide exact line-level evidence from the supplied code. "
            "Do not invent vulnerabilities or code that is not present."
        ),
        backstory=(
            "You are a senior applied-cryptography auditor specializing in "
            "post-quantum migration. You understand Shor's algorithm, Grover's "
            "algorithm, and current NIST post-quantum cryptography standards. "
            "NIST FIPS 203 defines ML-KEM, FIPS 204 defines ML-DSA, and "
            "FIPS 205 defines SLH-DSA. "
            "Use these current NIST names in recommendations. "
            "Do not present Kyber or Dilithium as the current official NIST "
            "standard names. Do not describe X25519, ECDH, ECC, RSA, or other "
            "classical public-key algorithms as post-quantum secure. "
            "Avoid speculative claims about when quantum computers will become "
            "capable of breaking cryptography. Clearly distinguish current "
            "classical weaknesses from future quantum threats."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def build_refactorer(llm: BaseLLM) -> Agent:
    return Agent(
        role="Post-Quantum Refactoring Engineer",
        goal=(
            "Rewrite the supplied vulnerable code using current NIST-standardized "
            "post-quantum cryptography. Use ML-KEM (FIPS 203) for key establishment "
            "and ML-DSA (FIPS 204) or SLH-DSA (FIPS 205) for digital signatures. "
            "Preserve the original functionality as closely as possible. "
            "Return a COMPLETE, syntactically valid implementation. "
            "Never stop in the middle of a function, class, comment, or code block."
        ),
        backstory=(
            "You are a senior post-quantum cryptography migration engineer. "
            "You understand NIST FIPS 203, FIPS 204, and FIPS 205. "
            "Use the Python package `pqcrypto` for the implementation. "
            "For ML-KEM use the documented `pqcrypto.kem.ml_kem_768` module. "
            "For ML-DSA use the documented `pqcrypto.sign.ml_dsa_65` module. "
            "Do not invent packages such as `mlkem` or `ml_dsa`. "
            "Do not invent functions such as generate_keypair(), encapsulate(), "
            "or decapsulate(). Use the documented pqcrypto API such as "
            "keygen(), encaps(), decaps(), sign(), and verify() where applicable. "
            "Always use the current names ML-KEM, ML-DSA, and SLH-DSA. "
            "Do not describe RSA, ECC, ECDH, X25519, DH, or DSA as post-quantum safe. "
            "Before finishing, check that every function has a complete body, "
            "all parentheses and strings are closed, all imports are present, "
            "and the entire code block is complete. "
            "If an exact API cannot be established, clearly mark the code "
            "as requiring verification instead of inventing an API."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

def build_verify_task(agent: Agent, context_tasks: list[Task], language: str) -> Task:
    return Task(
        description=(
            f"Strictly verify the COMPLETE refactored {language} code from the "
            "previous Refactorer task.\n\n"

            "You MUST inspect both the audit report and the complete refactored "
            "code before giving your verdict.\n\n"

            "Verification requirements:\n"
            "1. Check Python syntax and completeness.\n"
            "2. Check every import and referenced function.\n"
            "3. Verify that all pqcrypto APIs used are consistent with the "
            "specified dependency.\n"
            "4. Check ML-KEM usage: key generation, encapsulation and decapsulation.\n"
            "5. Check ML-DSA usage: key generation, signing and verification.\n"
            "6. Check AES-GCM key length, nonce handling and ciphertext handling.\n"
            "7. Check that RSA, ECC, ECDH, DH, DSA and SHA-1 are removed.\n"
            "8. Check NIST terminology: ML-KEM FIPS 203, ML-DSA FIPS 204, "
            "SLH-DSA FIPS 205.\n"
            "9. Check for missing signature verification functionality.\n"
            "10. Check key management, serialization and error handling.\n"
            "11. Do not assume an AI-generated API is valid merely because "
            "the code looks syntactically correct.\n"
            "12. If an external package/API requires confirmation, mark it "
            "as a warning instead of silently approving it.\n\n"

            "Your response MUST begin with exactly one of these lines:\n"
            "VERDICT: PASS\n"
            "VERDICT: PASS WITH WARNINGS\n"
            "VERDICT: FAIL\n\n"

            "After the verdict, provide:\n"
            "- Verification checklist\n"
            "- Issues found\n"
            "- Required fixes\n"
            "- Readiness summary\n\n"

            "IMPORTANT: Always return a non-empty verification report. "
            "Never return an empty response."
        ),
        expected_output=(
            "A non-empty Markdown verification report beginning with exactly "
            "'VERDICT: PASS', 'VERDICT: PASS WITH WARNINGS', or 'VERDICT: FAIL'."
        ),
        agent=agent,
        context=context_tasks,
    )
