import streamlit as st
from src.generator import generate_quiz
from src.pdf_generator import create_pdf
from src.history import save_attempt, load_history
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
from src.utils import (
    calculate_percentage,
    format_time,
    get_performance_message
)
import time


def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

#st.image("assets/logo.png",width=120)

st.markdown(
    """
    <div class="main-title">
        AI Sports Quiz Generator
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-title">
        Generate AI-powered sports quizzes using Retrieval-Augmented Generation (RAG)
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Quiz",
        "History",
        "Leaderboard"
    ]
)

# ---------------- Dashboard ----------------

if page == "Dashboard":

    st.header("Dashboard")

    history = load_history()

    attempts = len(history)

    highest = 0
    average = 0

    if attempts:

        scores = [
            h["score"] / h["total"] * 100
            for h in history
        ]

        highest = max(scores)
        average = sum(scores) / attempts

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Highest Score",
            f"{highest:.0f}%"
        )

        st.metric(
            "Attempts",
            attempts
        )

    with col2:

        st.metric(
            "Average",
            f"{average:.0f}%"
        )

    if attempts:

        latest = history[-1]

        st.metric(
            "Last Score",
            f"{latest['score']}/{latest['total']}"
        )
    st.info("Choose Quiz from the sidebar to start.")


# ---------- Session State ----------
if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if page == "Quiz":

# ---------- Sidebar ----------
    st.sidebar.header("Quiz Settings")

    sport = st.sidebar.selectbox(
        "Select Sport",
        ["Cricket", "Football", "Badminton", "Tennis"]
   )

    num_questions = st.sidebar.slider(
        "Number of Questions",
        1,
        10,
        3
    )

    difficulty = st.sidebar.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    # ---------- Generate Quiz ----------
    if st.sidebar.button("Generate Quiz"):

        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.start_time = time.time()
        st.session_state.submitted = False

        with st.spinner("Generating Quiz..."):

            st.session_state.quiz = generate_quiz(
                sport,
                num_questions,
                difficulty
            )

    # ---------- Display Quiz ----------
    if st.session_state.quiz:

        st_autorefresh(interval=1000, key="timer")
        total = len(st.session_state.quiz)
        current = st.session_state.current_question

        progress = (current + 1) / total
        st.progress(progress)

        st.subheader(f"Question {current + 1} of {total}")

        question = st.session_state.quiz[current]

        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)

        st.write(question["question"])

        selected = st.radio(
            "Choose one option",
            question["options"],
            key=f"question_{current}"
        )

        st.session_state.answers[current] = selected

        st.markdown("</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            if current > 0:
                if st.button("⬅ Previous"):
                    st.session_state.current_question -= 1
                    st.rerun()

        with col2:
            if current < total - 1:
                if st.button("Next ➡"):
                    st.session_state.current_question += 1
                    st.rerun()



        if st.session_state.start_time:

            time_limit = 300  # 5 minutes

            elapsed = int(time.time() - st.session_state.start_time)

            remaining = max(time_limit - elapsed, 0)

            st.sidebar.metric(
                "Remaining Time",
                format_time(remaining)
            )


            if remaining == 0:

                st.warning("⏰ Time is up!")

                st.session_state.submitted = True

        # ---------- Submit ----------
        if current == total - 1:

            if st.button("Submit Quiz"):
                st.session_state.submitted = True

            if st.session_state.submitted:

                score = 0

                st.header("Results")

                for i, q in enumerate(st.session_state.quiz):

                    if st.session_state.answers.get(i) == q["answer"]:

                        score += 1

                        st.success(f"Question {i+1}: Correct")

                    else:

                        st.error(f"Question {i+1}: Incorrect")

                        st.write(f"Correct Answer: **{q['answer']}**")
                        st.info(q["explanation"])
                        st.divider()

                    percentage = calculate_percentage(score, total)

                    correct = score
                    wrong = total - score

                    fig, ax = plt.subplots()

                    ax.pie(
                        [correct, wrong],
                        labels=["Correct", "Wrong"],
                        autopct="%1.1f%%"
                    )

                    st.pyplot(fig)

                    save_attempt(
                        sport,
                        difficulty,
                        score,
                        total
                    )

                    if percentage >= 80:
                        st.balloons()

                    message = get_performance_message(percentage)

                    if percentage >= 80:
                        st.success(message)

                    elif percentage >= 60:
                        st.info(message)

                    else:
                        st.warning(message)

                    st.sidebar.metric(
                        "Questions",
                        total
                    )

                    st.sidebar.metric(
                        "Score",
                        f"{score}/{total}"
                    )

                    st.sidebar.metric(
                        "Percentage",
                        f"{percentage:.0f}%"
                )

                    st.markdown(
                        f"""
                        <div class="score-card">
                            Final Score<br>
                            {score}/{total}<br>
                            ({percentage:.0f}%)
                        </div>
                        """,
                        unsafe_allow_html=True,
                )

                    pdf_file = create_pdf(
                        st.session_state.quiz,
                        st.session_state.answers,
                        score
                    )

                    with open(pdf_file, "rb") as file:

                        st.download_button(
                            "Download Result",
                            data=file,
                            file_name="quiz_result.pdf",
                            mime="application/pdf",
                            key="download_pdf"
                        )

                    st.subheader(" Quiz Analytics")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Questions", total)

                    with col2:
                        st.metric("Correct", score)

                    with col3:
                        st.metric("Wrong", total - score)

                    st.progress(score / total)

                    st.divider()

if page == "📜 History":

    st.header("📜 Quiz History")

    history = load_history()

    if history:

        for item in reversed(history):

            st.write(
                f"{item['date']} | "
                f"{item['sport']} | "
                f"{item['difficulty']} | "
                f"{item['score']}/{item['total']}"
            )

    else:

        st.info("No quiz history available.")  

if page == "Leaderboard":

    st.header("Leaderboard")

    history = load_history()

    if history:

        history.sort(
            key=lambda x: x["score"] / x["total"],
            reverse=True
        )

        leaderboard = []

        for item in history:

            leaderboard.append(
                {
                    "Sport": item["sport"],
                    "Difficulty": item["difficulty"],
                    "Score": f"{item['score']}/{item['total']}",
                    "Percentage": f"{item['score']/item['total']*100:.0f}%"
                }
            )

        st.dataframe(
            leaderboard,
            use_container_width=True
        )

    else:

        st.info("No leaderboard data yet.")  

st.divider()

st.subheader("📈 Performance Chart")

history = load_history()

if history:

    scores = [
        item["score"] / item["total"] * 100
        for item in history
    ]

    attempts = list(range(1, len(scores) + 1))

    fig, ax = plt.subplots(figsize=(8,4))

    ax.plot(
        attempts,
        scores,
        marker="o"
    )

    ax.set_xlabel("Quiz Attempt")
    ax.set_ylabel("Percentage")
    ax.set_title("Performance Over Time")

    st.pyplot(fig)


