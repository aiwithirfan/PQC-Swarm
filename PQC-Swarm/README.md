# 🛡️ PQC-Swarm
### Autonomous Agentic System for Post-Quantum Cryptographic Migration

Quantum computers running Shor's algorithm will break RSA, ECC, DH and DSA. Organizations must migrate, but finding and rewriting legacy crypto by hand is slow and error-prone. **PQC-Swarm** automates it with three cooperating AI agents.

## How it works

| Agent | Job |
|---|---|
| **Quantum Vulnerability Auditor** | Scans the pasted code and reports quantum-vulnerable primitives with severity and location |
| **Post-Quantum Refactoring Engineer** | Rewrites the code with NIST-standardized algorithms: ML-KEM (FIPS 203), ML-DSA (FIPS 204), SLH-DSA (FIPS 205), plus AES-256-GCM and SHA-384 |
| **Code Verification & Readiness Analyst** | Reviews syntax, imports, API usage and leftover legacy crypto, then issues a PASS / PASS WITH WARNINGS / FAIL verdict |

The agents run as a sequential [CrewAI](https://github.com/crewAIInc/crewAI) workflow. Each agent receives the previous agents' output as context. LLM inference runs on [Groq](https://groq.com) through `langchain-groq`.

## Project structure

```
app.py            Streamlit UI, custom CSS, Lottie animation
agents.py         CrewAI agents (role, goal, backstory)
tasks.py          CrewAI tasks for audit, refactor, verify
crew.py           Sequential crew assembly and runner
llm.py            Adapter exposing langchain-groq ChatGroq to CrewAI 1.x
requirements.txt  Pinned dependencies
.streamlit/config.toml   Dark theme, cyan/purple palette
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repository (keep `app.py` at the repository root).
2. On [share.streamlit.io](https://share.streamlit.io) choose **Create app**, select the repository, and set the main file to `app.py`.
3. Under **Advanced settings**, select **Python 3.12**.
4. Deploy. Enter your Groq API key in the app sidebar.

Optional: add `GROQ_API_KEY = "gsk_..."` under **Settings → Secrets** so the sidebar field can stay empty. Never commit keys to the repository.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Security notes

- The API key is entered through a password field and held only in the session.
- Pasted code is sent to Groq for analysis. Do not paste production secrets or private keys.
- AI output must be reviewed by a human and tested before production use. The Verifier performs a static review; it does not execute the code.

## Tech stack

Streamlit · CrewAI · LangChain-Groq · Streamlit-Lottie · Groq-hosted Llama models
