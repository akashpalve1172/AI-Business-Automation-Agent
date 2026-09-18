import streamlit as st
from langgraph_workflow import run_assistant


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TechNova AI Business Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# MODERN DARK THEME
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       APP BACKGROUND
    ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(99, 102, 241, 0.16),
                transparent 25%
            ),
            radial-gradient(
                circle at 95% 15%,
                rgba(139, 92, 246, 0.14),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #080d1a 0%,
                #0f172a 50%,
                #171127 100%
            );
    }


    /* =====================================================
       MAIN CONTAINER
    ===================================================== */

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       TEXT
    ===================================================== */

    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }

    p, label {
        color: #cbd5e1 !important;
    }


    /* =====================================================
       SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #070b14 0%,
                #111827 100%
            );

        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }


    /* =====================================================
       DIVIDERS
    ===================================================== */

    hr {
        border-color: rgba(255,255,255,0.10) !important;
    }


    /* =====================================================
       INPUTS
    ===================================================== */

    textarea,
    input {
        background-color: #172033 !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #94a3b8 !important;
    }


    /* =====================================================
       SELECTBOX
    ===================================================== */

    div[data-baseweb="select"] > div {
        background-color: #172033 !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }


    /* =====================================================
       BUTTON
    ===================================================== */

    div.stButton > button {
        width: 100%;
        min-height: 48px;

        border-radius: 12px;
        border: 1px solid #7c3aed !important;

        background:
            linear-gradient(
                90deg,
                #4f46e5,
                #7c3aed
            ) !important;

        color: white !important;
        font-weight: 700;
        font-size: 15px;

        box-shadow:
            0 8px 25px rgba(79, 70, 229, 0.25);
    }

    div.stButton > button:hover {
        background:
            linear-gradient(
                90deg,
                #6366f1,
                #8b5cf6
            ) !important;

        border-color: #a78bfa !important;
    }


    /* =====================================================
       CAPABILITY CARDS
    ===================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            rgba(20, 30, 48, 0.78);

        border: 1px solid rgba(148, 163, 184, 0.17);
        border-radius: 16px;
    }


    /* =====================================================
       ANSWER / CODE BLOCK
    ===================================================== */

    div[data-testid="stCodeBlock"] {
        border-radius: 12px;
    }

    pre {
        background-color: #0b1220 !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }


    /* =====================================================
       ALERTS
    ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* =====================================================
       FOOTER
    ===================================================== */

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🤖 TechNova")

    st.caption("AI Business Assistant")

    st.divider()

    st.markdown("### ⚡ Capabilities")

    st.write("📚  Policy Q&A")
    st.write("👥  Employee Data")
    st.write("🧮  Business Calculations")
    st.write("⚙️  Workflow Automation")
    st.write("✅  Result Validation")

    st.divider()

    st.markdown("### 🟢 System")

    st.success("System Online")

    st.divider()

    st.caption("Technology Stack")
    st.caption("Gemini")
    st.caption("LangGraph")
    st.caption("LangChain")
    st.caption("SQLite")


# =========================================================
# HEADER
# =========================================================

col1, col2 = st.columns(
    [5, 1]
)

with col1:

    st.markdown(
        "# 🤖 TechNova AI Business Assistant"
    )

    st.caption(
        "Enterprise AI assistant for company policies, "
        "employee data, calculations and operational workflows."
    )


with col2:

    st.success("● ONLINE")


st.divider()


# =========================================================
# AI CAPABILITIES
# =========================================================

st.markdown("## ✨ AI Capabilities")

col1, col2, col3, col4 = st.columns(4)


with col1:

    with st.container(border=True):

        st.markdown("### 📚")

        st.markdown("**Policy Q&A**")

        st.caption(
            "Search and retrieve company policies"
        )


with col2:

    with st.container(border=True):

        st.markdown("### 👥")

        st.markdown("**Employee Data**")

        st.caption(
            "Query structured employee records"
        )


with col3:

    with st.container(border=True):

        st.markdown("### 🧮")

        st.markdown("**Calculations**")

        st.caption(
            "Perform business calculations"
        )


with col4:

    with st.container(border=True):

        st.markdown("### ⚙️")

        st.markdown("**Workflows**")

        st.caption(
            "Process operational requests"
        )


st.write("")


# =========================================================
# ASSISTANT
# =========================================================

st.markdown("## 💬 Ask the Assistant")

example_questions = [
    "Type your own question",
    "How many days can employees work from home?",
    "Show me employees from the IT department",
    "What is 4000 multiplied by 3?",
    "My company laptop was lost."
]


selected_question = st.selectbox(
    "Quick examples",
    example_questions
)


# =========================================================
# QUESTION INPUT
# =========================================================

if selected_question == "Type your own question":

    question = st.text_area(
        "Your question",
        placeholder=(
            "Ask about policies, employee data, "
            "calculations or business workflows..."
        ),
        height=110
    )

else:

    question = st.text_area(
        "Your question",
        value=selected_question,
        height=110
    )


# =========================================================
# RUN BUTTON
# =========================================================

run_button = st.button(
    "🚀 Run AI Assistant",
    type="primary",
    use_container_width=True
)


# =========================================================
# PROCESS REQUEST
# =========================================================

if run_button:

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "AI Assistant is processing your request..."
        ):

            try:

                response = run_assistant(
                    question
                )

                route = response.get(
                    "route",
                    "unknown"
                )

                final_answer = response.get(
                    "final_answer",
                    "No result."
                )

                validation_status = response.get(
                    "validation_status",
                    "unknown"
                )

                validation_message = response.get(
                    "validation_message",
                    ""
                )


                # =============================================
                # ROUTE
                # =============================================

                st.markdown(
                    f"### 🔀 Detected Route: `{route.upper()}`"
                )


                # =============================================
                # ANSWER
                # =============================================

                st.markdown("### 🧠 AI Response")


                # ---------------------------------------------
                # RAG
                # ---------------------------------------------

                if route == "rag":

                    lines = final_answer.split(
                        "\n",
                        1
                    )

                    source = lines[0].strip()

                    answer = (
                        lines[1].strip()
                        if len(lines) > 1
                        else final_answer.strip()
                    )

                    st.info(
                        f"📄 {source}"
                    )

                    st.markdown(
                        f"### {answer}"
                    )


                # ---------------------------------------------
                # SQL
                # ---------------------------------------------

                elif route == "sql":

                    st.code(
                        final_answer,
                        language="text"
                    )


                # ---------------------------------------------
                # CALCULATOR
                # ---------------------------------------------

                elif route == "calculator":

                    st.success(
                        f"🧮 {final_answer}"
                    )


                # ---------------------------------------------
                # WORKFLOW
                # ---------------------------------------------

                elif route == "workflow":

                    st.info(
                        final_answer
                    )


                # ---------------------------------------------
                # UNKNOWN
                # ---------------------------------------------

                else:

                    st.warning(
                        final_answer
                    )


                # =============================================
                # VALIDATION
                # =============================================

                st.markdown("### ✅ Validation")


                if validation_status == "passed":

                    st.success(
                        f"Validation Passed — "
                        f"{validation_message}"
                    )

                elif validation_status == "warning":

                    st.warning(
                        f"Validation Warning — "
                        f"{validation_message}"
                    )

                else:

                    st.error(
                        f"Validation Failed — "
                        f"{validation_message}"
                    )


            except Exception as e:

                st.error(
                    "An error occurred while processing the request."
                )

                with st.expander(
                    "Technical Details"
                ):

                    st.code(
                        str(e)
                    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "TechNova AI Business Assistant  •  "
    "Gemini  •  LangGraph  •  LangChain  •  SQLite"
)