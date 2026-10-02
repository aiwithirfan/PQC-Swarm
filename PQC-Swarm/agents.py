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


def build_refactor_task(agent: Agent, context_tasks: list[Task], code: str, language: str) -> Task:
    return Task(
        description=(
            f"Using the audit report, rewrite the original {language} code so every "
            "quantum-vulnerable primitive is replaced with a NIST-standardized "
            "post-quantum alternative.\n\n"
            f"Original code:\n```\n{code}\n```\n\n"
            "IMPORTANT IMPLEMENTATION RULES:\n"
            "1. Use the Python package `pqcrypto` for post-quantum cryptography.\n"
            "2. Use `pqcrypto.kem.ml_kem_768` for ML-KEM (NIST FIPS 203).\n"
            "3. Use `pqcrypto.sign.ml_dsa_65` for ML-DSA (NIST FIPS 204).\n"
            "4. Do NOT invent packages such as `mlkem` or `ml_dsa`.\n"
            "5. Do NOT invent functions such as `generate_keypair()`, "
            "`encapsulate()`, or `decapsulate()`.\n"
            "6. Use the actual documented pqcrypto API such as `keygen()`, "
            "`encaps()`, `decaps()`, `sign()`, and `verify()` where applicable.\n"
            "7. Keep the original function names and behavior where possible.\n"
            "8. Add short comments explaining each cryptographic migration.\n"
            "9. Put `pqcrypto==1.0.0` in a pip-install comment at the top.\n"
            "10. Return ONE complete Python code block. Never leave a function, "
            "string, parenthesis, or code block incomplete.\n"
            "11. After the code block, provide a short bullet list of changes."
        ),
        expected_output=(
            "A single complete Python code block using documented pqcrypto APIs, "
            "followed by a brief change summary."
        ),
        agent=agent,
        context=context_tasks,
    )
def build_verifier(llm: BaseLLM) -> Agent:
    return Agent(
        role="Code Verification & Readiness Analyst",
        goal=(
            "Strictly verify the complete refactored code for syntax errors, "
            "undefined names, invalid imports, incorrect cryptographic APIs, "
            "incomplete functions, remaining RSA/ECC/DH/DSA/SHA-1 usage, "
            "incorrect NIST terminology, and security design problems. "
            "Return PASS only when the supplied implementation is internally "
            "consistent and its cryptographic APIs are clearly supported by "
            "the stated dependency. Return PASS WITH WARNINGS when the code "
            "is structurally correct but an external dependency or API requires "
            "verification. Return FAIL when the code is incomplete, syntactically "
            "invalid, uses unsupported APIs as if they were confirmed, or "
            "contains a serious cryptographic error."
        ),
        backstory=(
            "You are a meticulous cryptography QA and DevSecOps reviewer. "
            "NIST FIPS 203 is ML-KEM, FIPS 204 is ML-DSA, and FIPS 205 is SLH-DSA. "
            "Never approve RSA, ECC, ECDH, X25519, DH, or DSA as post-quantum "
            "replacements. Never assume that an AI-generated Python API exists. "
            "Check every import, function, method, parameter, return value, "
            "key-generation operation, encapsulation/decapsulation operation, "
            "signature operation, verification operation, KDF, AES-GCM usage, "
            "error handling, and serialization requirement. "
            "If an API cannot be established from the supplied code and dependency, "
            "explicitly mark it as requiring external verification. "
            "Do not claim that code is production-ready merely because it looks "
            "syntactically correct."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )
