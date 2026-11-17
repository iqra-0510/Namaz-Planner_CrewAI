"""Streamlit web app for the Namaz & Daily Ibadah Planner.  Run:  streamlit run app.py"""
import streamlit as st
from ibadah_crew import run_ibadah_crew, CITIES

st.set_page_config(page_title="Namaz & Ibadah Planner", page_icon="🕌", layout="wide")
st.title("🕌 Namaz & Daily Ibadah Planner")
st.caption("A team of 3 AI agents: Prayer Time Planner → Routine Writer → Routine Reviewer")
st.warning("Prayer times here are SAMPLE (fake) data for learning. For real times use a trusted app or mosque "
           "timetable, and ask a scholar for religious rulings.")

# ---------------- sidebar ----------------
with st.sidebar:
    st.header("Your day")
    city = st.selectbox("City", CITIES)
    work_hours = st.slider("Work hours", 0, 12, 8)
    quran_minutes = st.slider("Quran reading (minutes)", 0, 120, 20, step=5)
    walk_minutes = st.slider("Walk (minutes)", 0, 120, 30, step=5)
    go = st.button("Make my plan", type="primary", use_container_width=True)

# ---------------- main ----------------
if not go:
    st.info("Choose your options in the sidebar and press **Make my plan**.")
else:
    try:
        with st.spinner("The agents are working... (this can take a minute)"):
            result = run_ibadah_crew(city, work_hours, quran_minutes, walk_minutes)
    except SystemExit as e:           # config.py stops with a message when the key is missing
        st.error(str(e))
        st.stop()
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.caption("If it says 429, Groq's free limit is reached. Wait a minute and try again.")
        st.stop()

    outputs = result.tasks_output
    tab_times, tab_plan, tab_review = st.tabs(["🕐 Prayer times", "📋 Daily plan", "✅ Review"])
    with tab_times:
        st.markdown(outputs[0].raw)
    with tab_plan:
        st.markdown(outputs[1].raw)
    with tab_review:
        st.markdown(outputs[2].raw)

    st.caption(f"Token usage: {result.token_usage}")
