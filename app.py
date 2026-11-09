
import os
import time
import json

import streamlit as st
from dotenv import load_dotenv
from google import genai


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="SmartStudy AI | Study Smarter",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------- GEMINI API SETUP ----------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        light-dark(#f8f7ff, #0b1118) 0%,
        light-dark(#f0edff, #111c22) 55%,
        light-dark(#fff7fc, #12201f) 100%
    );
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

main[data-testid="stMain"] [data-testid="stMarkdownContainer"] > p,
main[data-testid="stMain"] [data-testid="stMarkdownContainer"] > ul li,
main[data-testid="stMain"] [data-testid="stMarkdownContainer"] > ol li,
main[data-testid="stMain"] label {
    color: light-dark(#30235c, #d5e5e2);
}

.hero {
    background: linear-gradient(
        120deg,
        light-dark(#6c4de6, #123d47),
        light-dark(#9875f5, #176c62)
    );
    padding: 38px;
    border-radius: 24px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 12px 35px light-dark(rgba(108, 77, 230, 0.20), rgba(0, 0, 0, 0.28));
}

.hero h1 {
    color: white;
    font-size: 2.6rem;
    font-weight: 800;
}

.hero p {
    color: #f3efff;
    font-size: 1.05rem;
}

.creator {
    color: #f6f0ff;
    font-size: 0.9rem;
    margin-top: 20px;
}

.section-title {
    color: light-dark(#30235c, #d5e5e2);
    font-size: 1.55rem;
    font-weight: 750;
    margin: 18px 0 6px 0;
}

.feature-card {
    background: light-dark(rgba(255, 255, 255, 0.90), #18262d);
    padding: 24px;
    border: 1px solid light-dark(#e6e0ff, #344b50);
    border-radius: 20px;
    box-shadow: 0 8px 24px light-dark(rgba(57, 39, 100, 0.06), rgba(0, 0, 0, 0.22));
    min-height: 135px;
    margin-bottom: 15px;
}

.feature-card h3 {
    color: light-dark(#4935a2, #91e2cf);
}

.feature-card p {
    color: light-dark(#69627d, #c2d1d1);
    font-size: 0.95rem;
}

div.stButton > button {
    background: linear-gradient(
        90deg,
        light-dark(#7454e8, #146f69),
        light-dark(#9975f6, #25a288)
    );
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.2rem;
    font-weight: 650;
}

div.stButton > button:hover {
    color: white;
    border: none;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px light-dark(rgba(116, 84, 232, 0.22), rgba(20, 111, 105, 0.30));
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    border-radius: 12px;
    border: 1px solid light-dark(#ddd5fa, #38515a);
    background: light-dark(#ffffff, #142129);
    color: light-dark(#2d1b4e, #e3f2ef);
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        light-dark(#111827, #101a21),
        light-dark(#1e1b4b, #142b2e)
    );
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #f8fafc;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white;
}

.footer {
    text-align: center;
    padding: 24px 10px;
    color: light-dark(#756b91, #a9bfbb);
    font-size: 0.9rem;
    border-top: 1px solid light-dark(#e6e0f7, #34464a);
    margin-top: 35px;
}

textarea {
    color: light-dark(#2d1b4e, #e3f2ef) !important;
    background-color: light-dark(#ffffff, #142129) !important;
    -webkit-text-fill-color: light-dark(#2d1b4e, #e3f2ef) !important;
    font-size: 16px !important;
}

textarea::placeholder {
    color: light-dark(#777777, #9bb1ae) !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 📚 SmartStudy AI")
    st.caption("Your personal study companion")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Home",
            "📖 Notes Summarizer",
            "🎯 Quiz Generator",
            "ℹ️ About Project"
        ]
    )

    st.markdown("---")
    st.markdown("### 👩🏻‍💻 ABOUT THE DEVELOPER")
    st.markdown("## 💜 mansiiieee06")
    st.markdown("**AIML Engineering Student**")
    st.caption("✨ Learning • Building • Innovating")


# ---------- HERO HEADER ----------
st.markdown("""
<div class="hero">
    <h1>📚 SmartStudy AI</h1>
    <p>Your personal study companion — learn smarter, every day.</p>
    <div class="creator">
        ✨ Developed by <b>mansiiieee06</b> · AIML Engineering Student
    </div>
</div>
""", unsafe_allow_html=True)


# ---------- HOME PAGE ----------
if page == "🏠 Home":

    st.markdown(
        '<div class="section-title">Welcome to your study space ✨</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Organise your learning, simplify your notes, "
        "and prepare for quizzes."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📖 Notes Summarizer</h3>
            <p>Turn long study notes into short, easy-to-review summaries using Gemini AI.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Quiz Generator</h3>
            <p>Choose a topic and prepare for your next study session.</p>
        </div>
        """, unsafe_allow_html=True)

    st.success("💡 Welcome to SmartStudy AI! Happy Learning.")


# ---------- NOTES SUMMARIZER ----------
elif page == "📖 Notes Summarizer":

    st.markdown(
        '<div class="section-title">📖 Notes Summarizer</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Paste your study notes below and let Gemini AI summarize them."
    )

    notes = st.text_area(
        "Your Study Notes",
        height=230,
        placeholder="Paste your notes here..."
    )

    sentence_count = st.slider(
        "Summary length (sentences)",
        min_value=1,
        max_value=8,
        value=3
    )

    if st.button("✨ Summarize Notes", use_container_width=True):

        if not notes.strip():
            st.warning("Please paste your notes first.")

        else:
            try:
                with st.spinner("🤖 Gemini AI is summarizing your notes..."):

                    response = None

                    # Retry up to 3 times for temporary 503 errors.
                    for attempt in range(3):
                        try:
                            response = client.models.generate_content(
                                model="gemini-3.8-flash",
                                contents=f"""
Summarize these study notes in simple English.

Give:
1. A suitable heading.
2. Important points.
3. Easy explanations.

Keep the summary approximately {sentence_count} sentences long.

Study Notes:
{notes}
"""
                            )
                            break

                        except Exception as api_error:
                            error_text = str(api_error)

                            is_temporary_error = (
                                "503" in error_text
                                or "UNAVAILABLE" in error_text
                            )

                            if is_temporary_error and attempt < 2:
                                time.sleep(5)
                            else:
                                raise

                summary = response.text if response else None

                if summary:
                    st.markdown("### 💡 Your AI Summary")
                    st.success(summary)

                    st.download_button(
                        "⬇️ Download Summary",
                        data=summary,
                        file_name="smartstudy_AI_summary.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Gemini returned an empty response.")

            except Exception as e:
                st.error(f"Gemini Error: {e}")



# ----------- QUIZ GENERATOR -----------
elif page == "🎯 Quiz Generator":

    st.markdown(
        '<div class="section-title">🎯 Quiz Generator</div>',
        unsafe_allow_html=True
    )

    st.write("Generate AI-powered MCQs for your study topic.")

    topic = st.text_input(
        "Study Topic",
        placeholder="e.g. Python Basics, Machine Learning..."
    )

    if st.button("✨ Generate Quiz", use_container_width=True):

        if topic.strip():

            try:
                with st.spinner("Generating your quiz..."):

                    prompt = f"""
                    Create exactly 5 multiple-choice questions
                    about: {topic}

                    Return ONLY valid JSON in this format:
                    {{
                      "questions": [
                        {{
                          "question": "Question text",
                          "options": ["A", "B", "C", "D"],
                          "answer": "Exact correct option",
                          "explanation": "Short explanation"
                        }}
                      ]
                    }}

                    Make questions educational and accurate.
                    """

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                    result = response.text.strip()
                    result = result.replace("```json", "")
                    result = result.replace("```", "")

                    quiz_data = json.loads(result)

                st.session_state["generated_quiz"] = quiz_data
                st.session_state["quiz_topic"] = topic

            except Exception as e:
                st.error(f"Quiz generation failed: {e}")

        else:
            st.warning("Please enter a study topic.")

    if "generated_quiz" in st.session_state:

        quiz_data = st.session_state["generated_quiz"]

        st.markdown("### 📝 Your AI Quiz")
        st.write(f"Topic: {st.session_state['quiz_topic']}")

        with st.form("quiz_answer_form"):

            user_answers = {}

            for i, question in enumerate(
                quiz_data["questions"]
            ):

                st.markdown(
                    f"**Q{i + 1}. {question['question']}**"
                )

                user_answers[i] = st.radio(
                    "Choose your answer:",
                    question["options"],
                    key=f"quiz_question_{i}",
                    index=None
                )

            submitted = st.form_submit_button(
                "✅ Submit Quiz"
            )

        if submitted:

            score = 0

            for i, question in enumerate(
                quiz_data["questions"]
            ):

                correct_answer = question["answer"]
                selected_answer = user_answers[i]

                if selected_answer == correct_answer:
                    score += 1
                    st.success(f"Q{i + 1}: Correct!")
                else:
                    st.error(
                        f"Q{i + 1}: Correct answer: "
                        f"{correct_answer}"
                    )

                st.write(
                    f"Explanation: {question['explanation']}"
                )

            st.markdown(
                f"### 🎉 Your Score: "
                f"{score}/{len(quiz_data['questions'])}"
            )



# ---------- ABOUT PROJECT ----------
elif page == "ℹ️ About Project":

    st.markdown(
        '<div class="section-title">ℹ️ About SmartStudy AI</div>',
        unsafe_allow_html=True
    )

    st.write("""
    SmartStudy AI is a student learning assistant project built
    using Python, Streamlit and Google's Gemini AI.

    It helps students simplify their study notes and organise
    their learning.
    """)

    st.markdown("### 🛠️ Technologies")
    st.write("- Python")
    st.write("- Streamlit")
    st.write("- Google Gemini API")
    st.write("- Python Dotenv")

    st.markdown("### 👩🏻‍💻 About the Developer")

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #211b3d, #49358c);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #8065d9;
        text-align: center;
    ">
        <div style="font-size: 38px;">👩🏻‍💻</div>
        <h2 style="color: #ffffff; margin-bottom: 8px;">
            mansiiieee06
        </h2>
        <p style="color: #e4dcff;">
            AIML Engineering Student
        </p>
        <p style="color: #c7b8ff; font-size: 13px;">
            Learning • Building • Innovating ✨
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚀 Future Improvements")
    st.write("- Automatically generated quizzes")
    st.write("- AI doubt-solving assistant")
    st.write("- Voice-based learning assistant")


# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    Made with 💜 using Python & Streamlit<br>
    SmartStudy AI · Developed by <b>mansiiieee06</b>
</div>
""", unsafe_allow_html=True)
