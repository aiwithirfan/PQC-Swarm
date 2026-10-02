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

    # Normal CrewAI TaskOutput
    raw = getattr(output, "raw", None)

    if raw is not None:
        text = str(raw).strip()
        if text:
            return text

    # Fallback: string representation
    try:
        text = str(output).strip()
        if text and text.lower() not in {"none", "null"}:
            return text
    except Exception:
        pass

    return ""


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

    # ------------------------------------------------------------------
    # Agents
    # ------------------------------------------------------------------
    auditor = build_auditor(llm)
    refactorer = build_refactorer(llm)
    verifier = build_verifier(llm)

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Progress callbacks
    # ------------------------------------------------------------------
    if on_step:
        t_audit.callback = lambda _output: on_step("Auditor finished")
        t_refactor.callback = lambda _output: on_step("Refactorer finished")
        t_verify.callback = lambda _output: on_step("Verifier finished")

    # ------------------------------------------------------------------
    # Sequential Crew
    # ------------------------------------------------------------------
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

    # Run all three agents
    crew.kickoff()

    # ------------------------------------------------------------------
    # Safely collect outputs
    # ------------------------------------------------------------------
    audit_output = _task_output_text(t_audit)
    refactor_output = _task_output_text(t_refactor)
    verification_output = _task_output_text(t_verify)

    # ------------------------------------------------------------------
    # Defensive verifier check
    # ------------------------------------------------------------------
    if not verification_output:
        verification_output = (
            "VERDICT: FAIL\n\n"
            "## Verification Error\n\n"
            "The Verifier agent completed without returning a readable "
            "verification report. The refactored code must not be considered "
            "verified or production-ready until the Verifier returns a "
            "non-empty report."
        )

    return SwarmResult(
        audit=audit_output,
        refactored=refactor_output,
        verification=verification_output,
    )
