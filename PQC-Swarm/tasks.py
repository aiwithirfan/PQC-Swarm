"""CrewAI task definitions for PQC-Swarm."""
from __future__ import annotations

from crewai import Agent, Task


def build_audit_task(agent: Agent, code: str, language: str) -> Task:
    return Task(
        description=(
            f"Audit the following {language} code for quantum-vulnerable cryptography.\n\n"
            f"```\n{code}\n```\n\n"
            "Produce a Markdown report with: (1) an executive summary and overall risk "
            "rating, (2) a table of findings with columns Finding | Location | Algorithm | "
            "Quantum Threat | Severity, (3) recommended NIST replacement for each finding. "
            "Only report issues actually present in the code."),
        expected_output="A structured Markdown audit report with a findings table and remediations.",
        agent=agent,
    )


def build_refactor_task(agent: Agent, context_tasks: list[Task], code: str, language: str) -> Task:
    return Task(
        description=(
            f"Using the audit report, rewrite the original {language} code so every "
            "quantum-vulnerable primitive is replaced with a NIST-approved post-quantum "
            "alternative (ML-KEM, ML-DSA, SLH-DSA) plus AES-256-GCM / SHA-384 where needed.\n\n"
            f"Original code:\n```\n{code}\n```\n\n"
            "Rules: keep the original function names and behavior where possible; add short "
            "comments explaining each change; list required pip packages in a comment at "
            "the top. Output ONE complete code block, then a short bullet list of changes."),
        expected_output="A single complete refactored code block followed by a brief change summary.",
        agent=agent, context=context_tasks,
    )


def build_verify_task(agent: Agent, context_tasks: list[Task], language: str) -> Task:
    return Task(
        description=(
            f"Review the refactored {language} code from the previous step. Check syntax, "
            "imports, API usage, leftover legacy crypto, error handling, and key handling. "
            "Begin your answer with exactly one verdict line: "
            "'VERDICT: PASS', 'VERDICT: PASS WITH WARNINGS', or 'VERDICT: FAIL'. "
            "Then give a Markdown checklist of checks performed, any issues found with "
            "suggested fixes, and a short readiness summary."),
        expected_output="A line starting with 'VERDICT:' followed by a Markdown verification report.",
        agent=agent, context=context_tasks,
    )
