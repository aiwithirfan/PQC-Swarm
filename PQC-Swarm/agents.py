"""CrewAI agent definitions for PQC-Swarm."""
from __future__ import annotations

from crewai import Agent, BaseLLM


def build_auditor(llm: BaseLLM) -> Agent:
    return Agent(
        role="Quantum Vulnerability Auditor",
        goal=(
            "Scan legacy source code and pinpoint every cryptographic primitive "
            "that a cryptographically relevant quantum computer could break or "
            "weaken, including RSA, ECC/ECDSA/ECDH, DH, DSA, and weak hashes "
            "or key sizes."
        ),
        backstory=(
            "You are a veteran applied-cryptography auditor who reviews "
            "banking and government systems. You understand Shor's and "
            "Grover's algorithms and follow NIST post-quantum cryptography "
            "standards. You cite line-level evidence, rate severity honestly, "
            "and never invent findings that are not present in the code."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def build_refactorer(llm: BaseLLM) -> Agent:
    return Agent(
        role="Post-Quantum Refactoring Engineer",
        goal=(
            "Rewrite vulnerable cryptographic code using NIST-standardized "
            "post-quantum cryptography. Use ML-KEM (FIPS 203) for key "
            "establishment, ML-DSA (FIPS 204) or SLH-DSA (FIPS 205) for "
            "digital signatures, and appropriate symmetric cryptography "
            "such as AES-256-GCM with secure hashing or KDFs. Preserve the "
            "original program's behavior and API as much as possible."
        ),
        backstory=(
            "You are a senior post-quantum cryptography migration engineer. "
            "You understand NIST FIPS 203, FIPS 204, and FIPS 205. "
            "Use the standardized names ML-KEM, ML-DSA, and SLH-DSA. "
            "Do not invent library APIs. Clearly identify when a required "
            "PQC library or API depends on the deployment environment. "
            "Produce practical, well-commented migration code and clearly "
            "mark any implementation assumptions."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def build_verifier(llm: BaseLLM) -> Agent:
    return Agent(
        role="Code Verification & Readiness Analyst",
        goal=(
            "Review the refactored code for syntax errors, undefined names, "
            "wrong imports, misuse of cryptographic APIs, leftover legacy "
            "algorithms, unsupported library APIs, and deployment risks. "
            "Then give a clear PASS / PASS WITH WARNINGS / FAIL verdict."
        ),
        backstory=(
            "You are a meticulous QA and DevSecOps lead. You mentally "
            "execute code line by line, check imports and API calls, "
            "verify cryptographic migration claims, and refuse to approve "
            "code that contains unsupported or invented APIs. "
            "You clearly distinguish verified functionality from assumptions "
            "that require local testing."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )
