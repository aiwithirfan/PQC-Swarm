"""Assembles the PQC-Swarm sequential crew."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from crewai import Crew, Process

from agents import build_auditor, build_refactorer, build_verifier
from llm import DEFAULT_MODEL, GroqChatLLM
from tasks import (
    build_audit_task,
    build_refactor_task,
    build_verify_task,
)


@dataclass
class SwarmResult:
    audit: str
    refactored: str
    verification: str


def _task_output_text(task) -> str:
    """Safely extract text from a CrewAI Task output."""
    output = getattr(task, "output", None)

    if output is None:
        return ""

    raw = getattr(output, "raw", None)

    if raw is not None:
        text = str(raw).strip()
        if text:
            return text

    try:
        text = str(output).strip()
        if text and text.lower() not in {"none", "null"}:
            return text
    except Exception:
        pass

    return ""


def _crew_output_text(crew_result, index: int) -> str:
    """Extract a task result from CrewOutput.tasks_output."""
    if crew_result is None:
        return ""

    outputs = getattr(crew_result, "tasks_output", None)

    if not outputs:
        return ""

    try:
        if index >= len(outputs):
            return ""

        output = outputs[index]

        raw = getattr(output, "raw", None)

        if raw is not None:
            text = str(raw).strip()
            if text:
                return text

        text = str(output).strip()

        if text and text.lower() not in {"none", "null"}:
            return text

    except Exception:
        pass

    return ""


def _direct_verification(
    llm,
    audit: str,
    refactored: str,
    language: str,
) -> str:
    """
    Fallback verifier.

    If CrewAI's third task does not expose a readable output,
    send the completed audit + refactored code directly to the
    configured LLM for verification.
    """

    verification_prompt = f"""
You are the final Code Verification & Readiness Analyst for PQC-Swarm.

Strictly verify the COMPLETE refactored {language} code below.

You MUST inspect the code itself. Do not merely trust the Refactorer.

AUDIT REPORT:
----------------
{audit}
----------------

REFACTORED CODE:
----------------
{refactored}
----------------

Verification requirements:

1. Check Python syntax and code completeness.

2. Check every import and referenced function.

3. Verify pqcrypto APIs against the specified Python pqcrypto dependency.

IMPORTANT:
For Python pqcrypto, the expected ML-KEM KEM API is:
- keygen()
- encaps()
- decaps()

Do NOT claim that encaps() or decaps() are invalid merely because
another cryptographic library uses names such as encapsulate()
or decapsulate().

4. Check ML-KEM key generation, encapsulation and decapsulation.

5. Check ML-DSA key generation, signing and verification.

6. Check AES-256-GCM key length, nonce handling, encryption
and decryption.

7. Check that the externally supplied session_key is actually
encrypted and recovered.

8. Check that RSA, ECC, ECDH, DH, DSA and SHA-1 have been removed
from the refactored code.

9. Check NIST terminology:
- ML-KEM = FIPS 203
- ML-DSA = FIPS 204
- SLH-DSA = FIPS 205

10. ML-DSA-65 is a valid FIPS 204 parameter set.
Do NOT mark ml_dsa_65 as non-compliant merely because it is
the 65 parameter set.

11. Check that signature verification functionality exists.

12. Check key management and serialization considerations.

13. Check error handling and input validation.

14. Do not invent alternative pqcrypto API names.

15. Distinguish actual code defects from production-readiness
warnings.

Your response MUST begin with exactly ONE of:

VERDICT: PASS

VERDICT: PASS WITH WARNINGS

VERDICT: FAIL

Then provide:

- Verification checklist
- Issues found
- Suggested fixes
- Readiness summary

Always return a complete non-empty verification report.
"""


    try:
        response = llm.call(
            [
                {
                    "role": "system",
                    "content": (
                        "You are a strict post-quantum cryptography "
                        "code verifier. Return only a useful verification "
                        "report and never return an empty response."
                    ),
                },
                {
                    "role": "user",
                    "content": verification_prompt,
                },
            ]
        )

        if response is None:
            return ""

        text = str(response).strip()

        # Remove accidental CrewAI-style wrapper if present.
        if "Final Answer:" in text:
            text = text.split("Final Answer:", 1)[1].strip()

        return text

    except Exception as exc:
        return (
            "VERDICT: FAIL\n\n"
            "## Verification Error\n\n"
            f"The fallback verifier could not complete verification: {exc}"
        )


def run_swarm(
    code: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    language: str = "Python",
    llm=None,
    on_step: Optional[Callable[[str], None]] = None,
) -> SwarmResult:

    if not code or not code.strip():
        raise ValueError("No code provided.")

    if llm is None:
        if not api_key or not api_key.strip():
            raise ValueError("A Groq API key is required.")

        llm = GroqChatLLM(
            api_key=api_key.strip(),
            model=model,
        )

    # ---------------------------------------------------------
    # Build agents
    # ---------------------------------------------------------

    auditor = build_auditor(llm)
    refactorer = build_refactorer(llm)
    verifier = build_verifier(llm)

    # ---------------------------------------------------------
    # Build tasks
    # ---------------------------------------------------------

    t_audit = build_audit_task(
        auditor,
        code,
        language,
    )

    t_refactor = build_refactor_task(
        refactorer,
        [t_audit],
        code,
        language,
    )

    t_verify = build_verify_task(
        verifier,
        [t_audit, t_refactor],
        language,
    )

    # ---------------------------------------------------------
    # Progress callbacks
    # ---------------------------------------------------------

    if on_step:
        t_audit.callback = lambda _output: on_step(
            "Auditor finished"
        )

        t_refactor.callback = lambda _output: on_step(
            "Refactorer finished"
        )

        t_verify.callback = lambda _output: on_step(
            "Verifier finished"
        )

    # ---------------------------------------------------------
    # Run CrewAI
    # ---------------------------------------------------------

    crew = Crew(
        agents=[
            auditor,
            refactorer,
            verifier,
        ],
        tasks=[
            t_audit,
            t_refactor,
            t_verify,
        ],
        process=Process.sequential,
        verbose=False,
    )

    crew_result = crew.kickoff()

    # ---------------------------------------------------------
    # Extract results
    # ---------------------------------------------------------

    audit_output = _task_output_text(t_audit)

    refactor_output = _task_output_text(t_refactor)

    verification_output = _task_output_text(t_verify)

    # CrewOutput fallback
    if not audit_output:
        audit_output = _crew_output_text(
            crew_result,
            0,
        )

    if not refactor_output:
        refactor_output = _crew_output_text(
            crew_result,
            1,
        )

    if not verification_output:
        verification_output = _crew_output_text(
            crew_result,
            2,
        )

    # ---------------------------------------------------------
    # IMPORTANT:
    # If CrewAI's Verifier task is empty, directly run the
    # verification through the same configured Groq LLM.
    # ---------------------------------------------------------

    if not verification_output:
        verification_output = _direct_verification(
            llm=llm,
            audit=audit_output,
            refactored=refactor_output,
            language=language,
        )

    # ---------------------------------------------------------
    # Final safety fallback
    # ---------------------------------------------------------

    if not verification_output:
        verification_output = (
            "VERDICT: FAIL\n\n"
            "## Verification Error\n\n"
            "The Verifier could not return a readable report."
        )

    # ---------------------------------------------------------
    # Return final swarm result
    # ---------------------------------------------------------

    return SwarmResult(
        audit=audit_output,
        refactored=refactor_output,
        verification=verification_output,
    )
