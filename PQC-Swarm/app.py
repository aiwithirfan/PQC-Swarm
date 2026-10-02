"""PQC-Swarm: Autonomous Agentic System for Post-Quantum Cryptographic Migration."""
from __future__ import annotations

import re

import requests
import streamlit as st
from streamlit_lottie import st_lottie

from llm import AVAILABLE_MODELS, DEFAULT_MODEL


st.set_page_config(
    page_title="PQC-Swarm",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root { --cyan:#00F0FF; --purple:#9D4DFF; --ink:#070B1A; --panel:#0F1530; --line:rgba(0,240,255,.25); }

html, body, [class*="css"], .stApp { font-family:'Space Grotesk',sans-serif; }

.stApp {
  background:
    radial-gradient(900px 500px at 85% -10%, rgba(157,77,255,.22), transparent 60%),
    radial-gradient(700px 420px at 0% 10%, rgba(0,240,255,.14), transparent 60%),
    var(--ink);
}

#MainMenu, footer { visibility:hidden; }

.block-container {
  padding-top:2rem;
  max-width:1200px;
}

/* Hero */
.hero-title {
  font-size:3.2rem;
  line-height:1.05;
  font-weight:700;
  letter-spacing:-.02em;
  margin:0 0 .6rem 0;
  background:linear-gradient(90deg,var(--cyan),var(--purple));
  -webkit-background-clip:text;
  background-clip:text;
  color:transparent;
}

.hero-sub {
  font-size:1.15rem;
  color:#B8C4E0;
  max-width:34rem;
  margin-bottom:1.2rem;
}

.chip {
  display:inline-block;
  padding:.28rem .75rem;
  margin:0 .4rem .4rem 0;
  border-radius:999px;
  border:1px solid var(--line);
  background:rgba(0,240,255,.07);
  color:#BFF8FF;
  font-size:.85rem;
}

/* Pipeline */
.pipeline {
  display:flex;
  gap:.8rem;
  align-items:stretch;
  margin:1.2rem 0 1.6rem 0;
  flex-wrap:wrap;
}

.node {
  flex:1 1 210px;
  padding:1rem 1.1rem;
  border-radius:14px;
  background:var(--panel);
  border:1px solid var(--line);
  box-shadow:0 0 18px rgba(0,240,255,.08);
}

.node:nth-child(2) {
  border-color:rgba(157,77,255,.45);
  box-shadow:0 0 18px rgba(157,77,255,.14);
}

.node h4 {
  margin:0 0 .25rem 0;
  color:#fff;
  font-size:1.02rem;
}

.node p {
  margin:0;
  color:#9FB0D3;
  font-size:.9rem;
}

.node.active {
  animation:pulse 1.4s ease-in-out infinite;
}

@keyframes pulse {
  50% {
    box-shadow:0 0 28px rgba(0,240,255,.45);
  }
}

/* Inputs */
.stTextArea textarea {
  font-family:'JetBrains Mono',monospace !important;
  font-size:.88rem !important;
  background:#0A1028 !important;
  color:#DDE8FF !important;
  border:1px solid var(--line) !important;
  border-radius:12px !important;
}

.stTextArea textarea:focus {
  border-color:var(--cyan) !important;
  box-shadow:0 0 0 1px var(--cyan),0 0 22px rgba(0,240,255,.35) !important;
}

section[data-testid="stSidebar"] {
  background:#0A0F25;
  border-right:1px solid var(--line);
}

section[data-testid="stSidebar"] input {
  border-radius:10px !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
  border-radius:12px;
  border:1px solid var(--line);
  background:#0F1736;
  color:#E6EDF7;
  font-weight:600;
  transition:box-shadow .2s ease, transform .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
  border-color:var(--cyan);
  box-shadow:0 0 16px rgba(0,240,255,.4);
}

.stButton > button[kind="primary"] {
  border:none;
  color:#04101C;
  font-size:1.05rem;
  padding:.7rem 1rem;
  background:linear-gradient(90deg,var(--cyan),var(--purple));
  box-shadow:0 0 22px rgba(0,240,255,.45), 0 0 44px rgba(157,77,255,.3);
}

.stButton > button[kind="primary"]:hover {
  transform:translateY(-1px);
  box-shadow:0 0 30px rgba(0,240,255,.7), 0 0 60px rgba(157,77,255,.5);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  gap:.4rem;
  border-bottom:1px solid var(--line);
}

.stTabs [data-baseweb="tab"] {
  border-radius:10px 10px 0 0;
  padding:.6rem 1.1rem;
  color:#9FB0D3;
}

.stTabs [aria-selected="true"] {
  color:var(--cyan) !important;
  background:rgba(0,240,255,.08);
}

.stTabs [data-baseweb="tab-highlight"] {
  background:linear-gradient(90deg,var(--cyan),var(--purple)) !important;
}

/* Result panel + verdict */
.panel {
  padding:1rem 1.2rem;
  border-radius:14px;
  background:var(--panel);
  border:1px solid var(--line);
}

.verdict {
  display:inline-block;
  padding:.45rem 1rem;
  border-radius:999px;
  font-weight:700;
  margin-bottom:1rem;
}

.v-pass {
  color:#06220F;
  background:#3DFFA2;
  box-shadow:0 0 18px rgba(61,255,162,.5);
}

.v-warn {
  color:#2A1D00;
  background:#FFC857;
  box-shadow:0 0 18px rgba(255,200,87,.5);
}

.v-fail {
  color:#2A0008;
  background:#FF5C7A;
  box-shadow:0 0 18px rgba(255,92,122,.5);
}

.v-unk {
  color:#E6EDF7;
  background:#38406A;
}

@media (prefers-reduced-motion: reduce) {
  .node.active {
    animation:none;
  }
}

@media (max-width:700px) {
  .hero-title {
    font-size:2.2rem;
  }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Lottie helpers
# ----------------------------------------------------------------------------
LOTTIE_URLS = [
    "https://assets10.lottiefiles.com/packages/lf20_w51pcehl.json",
    "https://assets3.lottiefiles.com/packages/lf20_kyu7xb1v.json",
]


def _fallback_lottie() -> dict:
    """Self-contained animation used if remote fetch fails."""

    def ring(radius, color, speed, dash, direction):
        return {
            "ty": 4,
            "nm": f"ring{radius}",
            "ip": 0,
            "op": 180,
            "st": 0,
            "sr": 1,
            "ind": radius,
            "ks": {
                "o": {"a": 0, "k": 100},
                "p": {"a": 0, "k": [200, 200, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]},
                "r": {
                    "a": 1,
                    "k": [
                        {
                            "t": 0,
                            "s": [0],
                            "i": {"x": [1], "y": [1]},
                            "o": {"x": [0], "y": [0]},
                        },
                        {
                            "t": 180,
                            "s": [360 * direction * speed],
                        },
                    ],
                },
            },
            "shapes": [
                {
                    "ty": "gr",
                    "it": [
                        {
                            "ty": "el",
                            "p": {"a": 0, "k": [0, 0]},
                            "s": {"a": 0, "k": [radius * 2, radius * 2]},
                        },
                        {
                            "ty": "st",
                            "c": {"a": 0, "k": color},
                            "o": {"a": 0, "k": 100},
                            "w": {"a": 0, "k": 5},
                            "lc": 2,
                            "lj": 2,
                            "d": [
                                {
                                    "n": "d",
                                    "nm": "d",
                                    "v": {"a": 0, "k": dash},
                                },
                                {
                                    "n": "g",
                                    "nm": "g",
                                    "v": {"a": 0, "k": dash * 0.7},
                                },
                            ],
                        },
                        {
                            "ty": "tr",
                            "p": {"a": 0, "k": [0, 0]},
                            "a": {"a": 0, "k": [0, 0]},
                            "s": {"a": 0, "k": [100, 100]},
                            "r": {"a": 0, "k": 0},
                            "o": {"a": 0, "k": 100},
                        },
                    ],
                }
            ],
        }

    core = {
        "ty": 4,
        "nm": "core",
        "ip": 0,
        "op": 180,
        "st": 0,
        "sr": 1,
        "ind": 99,
        "ks": {
            "o": {"a": 0, "k": 100},
            "p": {"a": 0, "k": [200, 200, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "r": {"a": 0, "k": 0},
            "s": {
                "a": 1,
                "k": [
                    {
                        "t": 0,
                        "s": [90, 90, 100],
                        "i": {"x": [0.5], "y": [1]},
                        "o": {"x": [0.5], "y": [0]},
                    },
                    {
                        "t": 90,
                        "s": [115, 115, 100],
                        "i": {"x": [0.5], "y": [1]},
                        "o": {"x": [0.5], "y": [0]},
                    },
                    {"t": 180, "s": [90, 90, 100]},
                ],
            },
        },
        "shapes": [
            {
                "ty": "gr",
                "it": [
                    {
                        "ty": "el",
                        "p": {"a": 0, "k": [0, 0]},
                        "s": {"a": 0, "k": [60, 60]},
                    },
                    {
                        "ty": "fl",
                        "c": {"a": 0, "k": [0.616, 0.302, 1, 1]},
                        "o": {"a": 0, "k": 100},
                    },
                    {
                        "ty": "tr",
                        "p": {"a": 0, "k": [0, 0]},
                        "a": {"a": 0, "k": [0, 0]},
                        "s": {"a": 0, "k": [100, 100]},
                        "r": {"a": 0, "k": 0},
                        "o": {"a": 0, "k": 100},
                    },
                ],
            }
        ],
    }

    return {
        "v": "5.7.0",
        "fr": 30,
        "ip": 0,
        "op": 180,
        "w": 400,
        "h": 400,
        "nm": "pqc",
        "ddd": 0,
        "assets": [],
        "layers": [
            core,
            ring(170, [0, 0.941, 1, 1], 1, 28, 1),
            ring(130, [0.616, 0.302, 1, 1], 1, 18, -1),
            ring(90, [0, 0.941, 1, 1], 2, 10, 1),
        ],
    }


@st.cache_data(show_spinner=False, ttl=86400)
def load_lottie() -> dict:
    for url in LOTTIE_URLS:
        try:
            r = requests.get(url, timeout=4)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict) and data.get("layers"):
                    return data
        except Exception:
            continue

    return _fallback_lottie()


# ----------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------
SAMPLE_CODE = '''from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1

# Legacy key exchange + signing (vulnerable to Shor's algorithm)
key = RSA.generate(2048)
public_key = key.publickey()

def encrypt_session_key(session_key: bytes) -> bytes:
    return PKCS1_OAEP.new(public_key).encrypt(session_key)

def decrypt_session_key(ciphertext: bytes) -> bytes:
    return PKCS1_OAEP.new(key).decrypt(ciphertext)

def sign_message(message: bytes) -> bytes:
    return pkcs1_15.new(key).sign(SHA1.new(message))
'''


LANGUAGES = [
    "Python",
    "Java",
    "JavaScript / Node.js",
    "Go",
    "C / C++",
    "C#",
    "Rust",
]

LANG_FENCE = {
    "Python": "python",
    "Java": "java",
    "JavaScript / Node.js": "javascript",
    "Go": "go",
    "C / C++": "cpp",
    "C#": "csharp",
    "Rust": "rust",
}


# ----------------------------------------------------------------------------
# State
# ----------------------------------------------------------------------------
st.session_state.setdefault("code_input", "")
st.session_state.setdefault("result", None)
st.session_state.setdefault("lang_used", "Python")


def _secret_key() -> str:
    try:
        return str(st.secrets.get("GROQ_API_KEY", ""))
    except Exception:
        return ""


def _load_sample() -> None:
    st.session_state["code_input"] = SAMPLE_CODE


def extract_code(text: str) -> str:
    match = re.search(r"```[\w+#-]*\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()


def parse_verdict(text: str) -> tuple[str, str, str]:
    m = re.search(
        r"VERDICT:\s*(PASS WITH WARNINGS|PASS|FAIL)",
        text.upper(),
    )

    if not m:
        return "UNRATED", "v-unk", "❔"

    v = m.group(1)

    if v == "PASS":
        return "PASS", "v-pass", "✅"

    if v == "PASS WITH WARNINGS":
        return "PASS WITH WARNINGS", "v-warn", "⚠️"

    return "FAIL", "v-fail", "❌"


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔐 Access")

    api_key = st.text_input(
        "Groq API key",
        type="password",
        placeholder="gsk_...",
        help="Used only for this session. Never stored or logged.",
    )

    if not api_key:
        api_key = _secret_key()

    st.caption("Get a free key at console.groq.com/keys")

    # Safe model selection
    default_index = (
        AVAILABLE_MODELS.index(DEFAULT_MODEL)
        if DEFAULT_MODEL in AVAILABLE_MODELS
        else 0
    )

    model = st.selectbox(
        "Model",
        AVAILABLE_MODELS,
        index=default_index,
    )

    language = st.selectbox("Source language", LANGUAGES)

    st.divider()

    st.markdown("### 🧬 Swarm")

    st.markdown(
        "**Auditor** finds quantum-vulnerable crypto  \n"
        "**Refactorer** migrates to ML-KEM / ML-DSA / SLH-DSA  \n"
        "**Verifier** checks syntax and readiness"
    )

    st.divider()
    st.caption("Standards: NIST FIPS 203 · 204 · 205")


# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
left, right = st.columns([1.35, 1], gap="large")

with left:
    st.markdown(
        '<h1 class="hero-title">PQC-Swarm</h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="hero-sub">Paste legacy RSA or ECC code. Three AI agents audit it, '
        'rewrite it with NIST post-quantum algorithms, and verify the result.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<span class="chip">ML-KEM · FIPS 203</span>'
        '<span class="chip">ML-DSA · FIPS 204</span>'
        '<span class="chip">SLH-DSA · FIPS 205</span>'
        '<span class="chip">Powered by Groq</span>',
        unsafe_allow_html=True,
    )

with right:
    st_lottie(
        load_lottie(),
        height=260,
        key="hero_lottie",
        speed=1,
        loop=True,
        quality="high",
    )


pipeline_slot = st.empty()


def render_pipeline(active: int = -1) -> None:
    items = [
        ("🔍 Auditor", "Flags RSA, ECC, DH and weak hashes"),
        ("🛠️ Refactorer", "Swaps in quantum-safe algorithms"),
        ("✅ Verifier", "Checks syntax and readiness"),
    ]

    html = '<div class="pipeline">'

    for i, (t, d) in enumerate(items):
        cls = "node active" if i == active else "node"
        html += (
            f'<div class="{cls}">'
            f"<h4>{t}</h4>"
            f"<p>{d}</p>"
            "</div>"
        )

    pipeline_slot.markdown(
        html + "</div>",
        unsafe_allow_html=True,
    )


render_pipeline()


# ----------------------------------------------------------------------------
# Input
# ----------------------------------------------------------------------------
st.markdown("#### Vulnerable code")

st.text_area(
    "Paste legacy cryptographic code",
    key="code_input",
    height=280,
    placeholder="# Paste RSA / ECC / DH / DSA code here...",
    label_visibility="collapsed",
)

c1, c2 = st.columns([1, 3])

c1.button(
    "Load sample code",
    on_click=_load_sample,
    use_container_width=True,
)

run = c2.button(
    "🚀 Run PQC-Swarm",
    type="primary",
    use_container_width=True,
)


# ----------------------------------------------------------------------------
# Execution
# ----------------------------------------------------------------------------
if run:
    code = st.session_state["code_input"]

    if not api_key:
        st.error("Add your Groq API key in the sidebar to start the swarm.")

    elif not code.strip():
        st.warning("Paste some code first, or choose Load sample code.")

    else:
        from crew import run_swarm

        st.toast("Swarm deployed", icon="🛰️")
        render_pipeline(0)

        def on_step(msg: str) -> None:
            try:
                st.toast(msg, icon="⚡")
            except Exception:
                pass

        try:
            with st.spinner(
                "Agents are auditing, refactoring and verifying your code..."
            ):
                st.session_state["result"] = run_swarm(
                    code=code,
                    api_key=api_key,
                    model=model,
                    language=language,
                    on_step=on_step,
                )

                st.session_state["lang_used"] = language

            render_pipeline()
            st.toast("Migration complete", icon="🎉")
            st.balloons()

        except Exception as exc:
            render_pipeline()

            msg = str(exc)

            if (
                "401" in msg
                or "invalid_api_key" in msg.lower()
                or "authentication" in msg.lower()
            ):
                st.error(
                    "Groq rejected the API key. Check it in the sidebar and try again."
                )

            elif "429" in msg or "rate" in msg.lower():
                st.error(
                    "Groq rate limit reached. Wait a minute or switch to another model."
                )

            else:
                st.error(
                    f"The swarm stopped before finishing: {msg[:400]}"
                )


# ----------------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------------
result = st.session_state["result"]

if result:
    st.markdown("#### Results")

    tab_audit, tab_code, tab_verify = st.tabs(
        [
            "🔍 Audit Report",
            "🛠️ Refactored Code",
            "✅ Verification Status",
        ]
    )

    fence = LANG_FENCE.get(
        st.session_state["lang_used"],
        "text",
    )

    with tab_audit:
        st.markdown(
            result.audit or "_No audit output was returned._"
        )

    with tab_code:
        code_only = extract_code(result.refactored)

        st.code(
            code_only,
            language=fence,
        )

        st.download_button(
            "Download refactored code",
            code_only,
            file_name="refactored_pqc.txt",
            mime="text/plain",
        )

        with st.expander("Full agent output with change summary"):
            st.markdown(result.refactored)

    with tab_verify:
        label, css, icon = parse_verdict(result.verification)

        st.markdown(
            f'<span class="verdict {css}">{icon} {label}</span>',
            unsafe_allow_html=True,
        )

        body = re.sub(
            r"^\s*VERDICT:.*\n?",
            "",
            result.verification,
            count=1,
            flags=re.IGNORECASE,
        )

        st.markdown(
            body or "_No verification output was returned._"
        )

    report = (
        f"# PQC-Swarm Report\n\n"
        f"## Audit\n{result.audit}\n\n"
        f"## Refactored Code\n{result.refactored}\n\n"
        f"## Verification\n{result.verification}\n"
    )

    st.download_button(
        "Download full report (.md)",
        report,
        file_name="pqc_swarm_report.md",
        mime="text/markdown",
    )

else:
    st.info("Results will appear here after the swarm finishes.")
