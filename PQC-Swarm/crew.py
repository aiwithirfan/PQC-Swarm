"""Assembles the PQC-Swarm sequential crew."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from crewai import Crew, Process

from agents import build_auditor, build_refactorer, build_verifier
from llm import DEFAULT_MODEL, GroqChatLLM
from tasks import build_audit_task, build_refactor_task, build_verify_task


@dataclass
class SwarmResult:
    audit: str
    refactored: str
    verification: str


def run_swarm(code: str, api_key: str, model: str = DEFAULT_MODEL,
              language: str = "Python", llm=None,
              on_step: Optional[Callable[[str], None]] = None) -> SwarmResult:
    """Run auditor -> refactorer -> verifier sequentially and return all outputs."""
    if not code or not code.strip():
        raise ValueError("No code provided.")
    if llm is None:
        if not api_key or not api_key.strip():
            raise ValueError("A Groq API key is required.")
        llm = GroqChatLLM(api_key=api_key.strip(), model=model)

    auditor, refactorer, verifier = build_auditor(llm), build_refactorer(llm), build_verifier(llm)
    t_audit = build_audit_task(auditor, code, language)
    t_refactor = build_refactor_task(refactorer, [t_audit], code, language)
    t_verify = build_verify_task(verifier, [t_audit, t_refactor], language)

    steps = {id(t_audit): "Auditor finished", id(t_refactor): "Refactorer finished",
             id(t_verify): "Verifier finished"}
    if on_step:
        for t in (t_audit, t_refactor, t_verify):
            t.callback = (lambda _o, msg=steps[id(t)]: on_step(msg))

    crew = Crew(agents=[auditor, refactorer, verifier],
                tasks=[t_audit, t_refactor, t_verify],
                process=Process.sequential, verbose=False)
    crew.kickoff()

    return SwarmResult(
        audit=(t_audit.output.raw if t_audit.output else ""),
        refactored=(t_refactor.output.raw if t_refactor.output else ""),
        verification=(t_verify.output.raw if t_verify.output else ""),
    )
