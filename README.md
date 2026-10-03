# 🔐 PQC-Swarm

**Autonomous Agentic System for Post-Quantum Cryptographic Migration**

PQC-Swarm is an agentic AI-powered security engineering system that automatically audits legacy cryptographic implementations, identifies quantum-vulnerable primitives, generates post-quantum replacements, and verifies the resulting code for cryptographic and implementation readiness.

---

## 🔗 Project Links

*   **🌐 Live Streamlit Application:** (https://pqc-swarm.streamlit.app/)
*   **📄 Professional PRD (Product Requirements Document):** [View PRD on Google Drive](https://drive.google.com/file/d/1Xh30n18Ok2SKeXtLHLbvwQ5QDF6dKHYR/view?usp=sharing)
*   **📊 Presentation Slides:** [View Slides on Google Drive](https://docs.google.com/presentation/d/1bjpYVhtTEDA_-v2OVWV2uxqZreMNqJR8/edit?usp=sharing&ouid=116962584390717046240&rtpof=true&sd=true)
*   **🎥 Project Demo & Presentation Video:** [Link to Demo Video - Add your Google Drive link here]

---

## 🚀 Overview

The emergence of sufficiently capable quantum computers presents a significant long-term threat to widely deployed public-key cryptography.

Algorithms such as:
*   RSA
*   ECC
*   ECDSA
*   ECDH
*   DH
*   DSA

are vulnerable to quantum attacks based on Shor's algorithm.

PQC-Swarm addresses this migration challenge through a coordinated multi-agent architecture that automates the transition from vulnerable classical cryptography toward NIST-standardized Post-Quantum Cryptography (PQC).

Instead of manually reviewing cryptographic code, developers can submit vulnerable source code and allow the agentic swarm to:

**Audit → Refactor → Verify**

---

## 🎯 Problem Statement

Modern software systems contain large amounts of legacy cryptographic code.

Manually migrating this code introduces several challenges:
*   Identifying every vulnerable cryptographic primitive
*   Selecting appropriate post-quantum replacements
*   Correctly implementing new cryptographic APIs
*   Preserving existing application behavior
*   Avoiding AI-generated cryptographic implementation errors
*   Verifying that legacy algorithms have actually been removed
*   Assessing code readiness after migration

PQC-Swarm provides an automated workflow to address these challenges.

---

## 💡 Solution

PQC-Swarm uses three specialized AI agents operating as a sequential security-engineering pipeline.

```text
┌─────────────────────┐
│ Vulnerable Code     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 🔍 AUDITOR AGENT    │
│                     │
│ Detects vulnerable  │
│ cryptographic       │
│ primitives          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 🔄 REFACTORER AGENT │
│                     │
│ Migrates legacy     │
│ crypto to NIST PQC  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ ✅ VERIFIER AGENT   │
│                     │
│ Checks syntax, APIs │
│ and PQC readiness   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Migration Report    │
│ + Refactored Code   │
│ + Verification      │
└─────────────────────┘
🧬 Multi-Agent Architecture
​1. 🔍 Quantum Vulnerability Auditor
​The Auditor analyzes submitted source code and identifies cryptographic weaknesses.
​Detects:
​RSA
​ECC
​ECDSA
​ECDH
​Diffie-Hellman
​DSA
​SHA-1
​Weak cryptographic constructions
​Insecure key sizes
​Output:
The Auditor produces a structured security report containing:
​Executive summary
​Risk assessment
​Vulnerability findings
​Exact code evidence
​Algorithm identification
​Quantum threat analysis
​Severity
​Recommended migration
​2. 🔄 Post-Quantum Refactoring Engineer
The Refactorer transforms vulnerable cryptographic implementations into post-quantum alternatives.
NIST Mapping:
Legacy CryptographyPQC Migration
RSA Key EstablishmentML-KEM
ECDHML-KEM
DHML-KEM
RSA SignaturesML-DSA
ECDSAML-DSA
DSAML-DSA
SHA-1Modern secure hashing strategy

Supported NIST Standards:
​FIPS 203 — ML-KEM
​FIPS 204 — ML-DSA
​FIPS 205 — SLH-DSA
​For the current implementation, PQC-Swarm uses ML-KEM-768 and ML-DSA-65 through the Python pqcrypto package.
​3. ✅ Code Verification & Readiness Analyst
​The Verifier independently reviews the generated implementation.
​It checks:
​Python syntax
​Import validity
​Function completeness
​Cryptographic API usage
​ML-KEM key generation
​ML-KEM encapsulation
​ML-KEM decapsulation
​ML-DSA signing
​ML-DSA verification
​AES-256-GCM usage
​Nonce handling
​Session-key recovery
​Legacy cryptography removal
​NIST terminology
​Key management considerations
​Input validation
​Error handling
​Verification Results:
The system can return:
VERDICT: PASS
or
VERDICT: PASS WITH WARNINGS
or
VERDICT: FAIL
​🛡️ Cryptographic Migration Model
​PQC-Swarm follows a hybrid cryptographic design when symmetric encryption is required.

​For example:
ML-KEM-768
    │
    ▼
Shared Secret
    │
    ▼
AES-256-GCM
    │
    ▼
Protected Data

Important Design Principle:
ML-KEM is a Key Encapsulation Mechanism (KEM). It establishes a shared secret; it does not directly encrypt arbitrary application plaintext.
​PQC-Swarm therefore uses the resulting shared secret with AES-256-GCM for symmetric encryption where appropriate.

​🧠 Agentic Workflow
    User Source Code
            │
            ▼
┌─────────────────────┐
│ Auditor             │
│ Vulnerability Scan  │
└─────────┬───────────┘
            │
            ▼
┌─────────────────────┐
│ Refactorer          │
│ PQC Transformation  │
└─────────┬───────────┘
            │
            ▼
┌─────────────────────┐
│ Verifier            │
│ Security Validation │
└─────────┬───────────┘
            │
            ▼
 Final Migratio
Output
​🛠️ Technology Stack
TechnologyPurpose
PythonCore application
StreamlitWeb interface
CrewAIMulti-agent orchestration
GroqLLM inference
LangChain GroqGroq integration
pqcryptoPost-quantum cryptographic primitives
cryptographyAES-256-GCM
NIST PQC StandardsCryptographic migration guidance

📁 Project Structure
PQC-Swarm/
│
├── app.py
├── agents.py
├── tasks.py
├── crew.py
├── llm.py
├── requirements.txt
├── README.md
│
└── assets/
    └── screenshots/

Core Components:
​app.py: Streamlit user interface and application workflow.
​agents.py: Defines the Auditor, Refactorer, and Verifier agents.
​tasks.py: Defines the specialized tasks executed by each agent.
​crew.py: Orchestrates the sequential multi-agent workflow.
​llm.py: Provides the CrewAI-compatible Groq LLM adapter.
​requirements.txt: Contains the project's Python dependencies.
​⚙️ Installation
​1. Clone the Repository
git clone (https://github.com/YOUR-USERNAME/PQC-Swarm.git)
cd PQC-Swarm
2. Create a Virtual Environment
python -m venv venv

Windows:
venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt

4. Configure Groq API
Create a Groq API key and provide it through the application's API-key field.
Never commit API keys to GitHub.
​▶️ Running the Application
​Start the Streamlit application:
streamlit run app.py
The application will open in your browser.
​🖥️ Application Workflow
Step 1 — Provide API Key: Enter your Groq API key.
Step 2 — Select Model: Choose the supported Groq model.
Step 3 — Select Language: Currently optimized for: Python
Step 4 — Submit Vulnerable Code:
Example:
from Crypto.PublicKey import RSA
key = RSA.generate(2048)
public_key = key.publickey()
Step 5 — Run Swarm: The three agents execute sequentially.
Step 6 — Review Results: The application provides:
​🔍 Audit Report
​🔄 Refactored Code
​✅ Verification Status
📊 Example Migration

​Before

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

key = RSA.generate(2048)
public_key = key.publickey()

def encrypt_session_key(session_key):
    return PKCS1_OAEP.new(public_key).encrypt(session_key)

After
from pqcrypto.kem import ml_kem_768
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

​🔐 Security Considerations
​PQC-Swarm is an AI-assisted cryptographic migration tool, not a replacement for expert security review.
​Generated code should be independently reviewed before deployment in production environments. Particular attention should be given to:
​Key lifecycle management
​Secure key storage
​Key serialization
​Error handling
​Input validation
​Cryptographic parameter selection
​Protocol-level security
​Authentication
​Certificate infrastructure
​Operational key rotation
​A successful AI verification result should not be interpreted as a formal security certification.
​⚠️ Current Limitations
​Python is currently the primary supported language.
​AI-generated migrations require human review.
​Production key-management integration is not included.
​The system does not perform formal mathematical verification of cryptographic implementations.
​Complex application-specific cryptographic protocols may require manual migration.
​Verification results depend partly on the underlying LLM analysis.
​🎯 Future Roadmap
​Phase 1 — Current
​[x] AI-powered vulnerability auditing
​[x] Multi-agent architecture
​[x] RSA detection
​[x] ECC/ECDSA detection
​[x] ECDH/DH detection
​[x] DSA detection
​[x] SHA-1 detection
​[x] ML-KEM migration
​[x] ML-DSA migration
​[x] Automated verification
​[x] Streamlit interface
​Phase 2
​[ ] C/C++ support
​[ ] Java support
​[ ] JavaScript/TypeScript support
​[ ] Go support
​[ ] Repository-level scanning
​[ ] GitHub integration
​[ ] Automated pull-request generation
​Phase 3
​[ ] Enterprise codebase analysis
​[ ] Cryptographic dependency graph
​[ ] Migration tracking dashboard
​[ ] CI/CD security integration
​[ ] Policy-based compliance reporting
​[ ] Automated migration recommendations
​📜 Standards Alignment
​PQC-Swarm is designed around the NIST Post-Quantum Cryptography standards:

StandardAlgorithmRole
FIPS 203ML-KEMKey Encapsulation
FIPS 204ML-DSADigital Signatures
FIPS 205SLH-DSAHash-Based Signatures

🧪 Testing Strategy
​PQC-Swarm can be tested against intentionally vulnerable cryptographic examples.
​Test Cases:
​RSA-2048 ↓ ML-KEM / ML-DSA
​ECC / ECDSA ↓ ML-DSA
​ECDH ↓ ML-KEM
​DH ↓ ML-KEM
​DSA ↓ ML-DSA
​SHA-1 ↓ Modern secure hashing strategy
​Each test should be evaluated across all three stages:
Detection → Migration → Verification
​🌐 Deployment
​PQC-Swarm can be deployed as a Streamlit application.
​Recommended deployment architecture:

      User
       │
       ▼
  Streamlit UI
       │
       ▼
CrewAI Orchestrator
       │
       ├── Auditor
       ├── Refactorer
       └── Verifier
       │
       ▼
    Groq LLM
       │
       ▼
PQC Migration Results

👥 Team
​PQC-Swarm Hackathon Team
​Project: PQC-Swarm
​Domain: Generative AI · Agentic AI · Cybersecurity · Post-Quantum Cryptography
​Team Leader: Irfan Shah
​Members: Ayesha Hasan, Muhammad Faran, Shayan Farrukh, Maryam Awan, Minahil Naveed

​🏆 Project Highlights
​🤖 Autonomous multi-agent security workflow
​🔍 Automated cryptographic vulnerability detection
​🔄 AI-assisted post-quantum migration
​🧬 NIST-aligned PQC implementation
​✅ Independent verification agent
​🔐 Cryptography-aware code generation
​📊 Structured security reporting
​⚡ Groq-powered inference
​🖥️ Interactive Streamlit interface
​⚖️ Disclaimer
​PQC-Swarm is an experimental/hackathon security engineering project intended for research, education, and assisted code migration.
​It should not be treated as a substitute for professional cryptographic engineering, formal security analysis, penetration testing, compliance validation, or independent code review.
​📄 License
​MIT License
​⭐ PQC-Swarm
Audit legacy cryptography.
Refactor for the post-quantum era.
Verify before deployment.
​Audit → Refactor → Verify
