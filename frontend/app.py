import streamlit as st
import requests
import datetime
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    
from agents.planner import StudyPlannerAgent
from skills.memory import MemorySkill

# Configure premium page layout & typography
st.set_page_config(
    page_title="Smart Study Planner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for vibrant colors, gradients, and premium look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4);
    }
    .recommendation-card {
        background-color: #1f2937;
        border-left: 5px solid #667eea;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .session-card {
        background-color: #111827;
        border: 1px solid #374151;
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Instantiations
agent = StudyPlannerAgent()
memory = MemorySkill()

# Sidebar Setup
st.sidebar.title("🤖 Study Assistant Chat")
st.sidebar.write("Ask questions about productivity, planning, or Google developer tools.")
chat_query = st.sidebar.text_input("Ask a question:")
if chat_query:
    with st.sidebar:
        with st.spinner("Thinking..."):
            # Call local agent's chat directly
            chat_response = agent.mcp_client.call_tool(
                "google-developer-knowledge",
                "answer_query",
                {"query": chat_query}
            )
            ans = chat_response.get("answer_text", "Focus on breaking study slots into 25-minute Pomodoro sessions.")
            st.info(ans)

st.title("📚 Smart Study Planner Agent")
st.write("Organize your revision schedules dynamically using Pomodoro cycles and exam dates.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Plan Configuration")
    
    # User Inputs
    subjects_input = st.text_input("Subjects (comma separated)", value="Math, History, Computer Science")
    exam_dates_input = st.text_area(
        "Exam Dates (YYYY-MM-DD format, one per line or JSON format)",
        value="Math: 2026-07-15\nHistory: 2026-07-18\nComputer Science: 2026-07-22"
    )
    hours_available = st.slider("Available study hours per day", min_value=0.5, max_value=12.0, value=3.0, step=0.5)
    
    # Process Inputs
    subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]
    
    exam_dates = {}
    for line in exam_dates_input.split("\n"):
        if ":" in line:
            parts = line.split(":")
            sub_key = parts[0].strip()
            date_val = parts[1].strip()
            if sub_key and date_val:
                exam_dates[sub_key] = date_val
                
    generate_clicked = st.button("🚀 Generate Study Plan")
    clear_history_clicked = st.button("🗑️ Clear Progress History")
    
    if clear_history_clicked:
        memory.clear_history()
        st.success("Study history cleared successfully!")
        st.rerun()

with col2:
    st.subheader("📅 Your Study Plan")
    
    # Retrieve active schedule from session state
    if "current_plan" not in st.session_state:
        st.session_state.current_plan = None
        
    if generate_clicked:
        try:
            # Generate plan using agent directly (guaranteeing it works without running FastAPI process)
            plan = agent.generate_plan(
                subjects=subjects,
                exam_dates=exam_dates,
                hours_available=hours_available
            )
            st.session_state.current_plan = plan
            st.success("Study plan generated successfully!")
        except ValueError as e:
            st.error(f"Validation Error: {str(e)}")
            
    if st.session_state.current_plan:
        plan = st.session_state.current_plan
        
        # Recommendations section
        st.write("### 💡 Recommendations")
        for rec in plan.get("recommendations", []):
            st.markdown(f"<div class='recommendation-card'><b>Tip:</b> {rec}</div>", unsafe_allow_html=True)
            
        # Schedule Timeline
        st.write("### 🗓️ Daily Schedule")
        
        # Keep track of completed items in UI
        completed_list = []
        
        for idx, day in enumerate(plan.get("schedule", [])):
            with st.expander(f"📅 {day['date']} ({day['day_of_week']})", expanded=(idx==0)):
                for slot_idx, slot in enumerate(day.get("slots", [])):
                    slot_id = f"{day['date']}_{slot['subject']}_{slot['type']}_{slot_idx}"
                    st.markdown(f"""
                    <div class='session-card'>
                        <b>{slot['start_time']} - {slot['end_time']}</b> | <b>{slot['subject']}</b> | {slot['type'].capitalize()} ({slot['duration_minutes']} mins)
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Checkbox to complete task
                    is_done = st.checkbox("Mark as completed", key=slot_id)
                    if is_done:
                        completed_list.append({
                            "date": day["date"],
                            "subject": slot["subject"],
                            "type": slot["type"],
                            "duration_minutes": slot["duration_minutes"],
                            "completed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        
        if completed_list:
            if st.button("✅ Submit Completed Tasks"):
                update_res = agent.update_plan(completed_list)
                st.success(f"Progress updated! Registered {len(completed_list)} study blocks.")
                st.rerun()

# Progress and History section
st.write("---")
st.subheader("📊 Your Study Progress Tracker")
history = memory.get_history()

if not history:
    st.info("No study sessions completed yet. Start completing blocks in your schedule above!")
else:
    total_mins = sum(h.get("duration_minutes", 0) for h in history)
    st.metric("Total Study Time Completed", f"{total_mins} minutes")
    
    # Progress bars for each subject
    sub_totals = {}
    for h in history:
        s = h.get("subject", "General")
        sub_totals[s] = sub_totals.get(s, 0) + h.get("duration_minutes", 0)
        
    st.write("#### Completion Breakdown by Subject:")
    for subject, minutes in sub_totals.items():
        st.write(f"**{subject}**: {minutes} mins")
        # Visual indicator
        st.progress(min(minutes / 300.0, 1.0)) # Scale to a target of 300 minutes per subject

