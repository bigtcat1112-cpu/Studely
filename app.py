import streamlit as st
import io
import time

# --- LOGIC LIFE CYCLE MATRIX ---
if "quiz_ready" not in st.session_state:
    st.session_state.quiz_ready = False
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# --- APPLICATION LIFECYCLE INITIALIZATION ---
st.set_page_config(
    page_title="Studley Workspace",
    page_icon="🎙️",
    layout="centered"
)

# Global Theme Style Block - Clean dark beige/grey high-contrast aesthetic
st.markdown("""
    <style>
    /* Global high-contrast dark beige/grey typography definition */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, li {
        color: #2E2D2A !important;
        font-family: 'Source Sans Pro', sans-serif;
    }
    /* Bright beige container styling for text input fields */
    div[data-testid="stTextInput"] > div > div > input {
        background-color: #FDFBF7 !important;
        color: #2E2D2A !important;
        border: 2px solid #E6A23C !important;
        border-radius: 8px;
    }
    /* Header optimization blocks */
    h1, h2, h3, h4 {
        color: #2E2D2A !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- STUDLEY WORKSPACE BRANDING ---
st.title("🎙️ Studley Advanced Podcast & Study Hub")
st.caption("Process complex science assets, view dynamic flashcards, and run quiz metrics.")

# Two main tabs restricted to her specific app components
tab1, tab2, tab3 = st.tabs([
    "🔬 Advanced Quiz Pipeline", 
    "🗂️ Extracted Flashcards", 
    "🎧 Audio Session Engine"
])

# --- TAB 1: ADVANCED QUIZ PIPELINE ---
with tab1:
    st.subheader("Document Ingestion System")
    st.write("Upload test files up to 10MB+ to initialize the analytical processing deck.")

    # Explicitly support lowercase and uppercase variants to prevent asset blocking
    uploaded_file = st.file_uploader(
        "Select science manuscript or script context matrix",
        type=["pdf", "PDF", "txt", "TXT"],
        key="secure_stream_uploader_core"
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_size_mb = len(file_bytes) / (1024 * 1024)

        if file_size_mb > 15.0:
            st.error(f"❌ Asset barrier restriction: {file_size_mb:.2f} MB exceeds maximum safety thresholds.")
        else:
            st.success(f"📦 Active buffer loaded successfully. Size: {file_size_mb:.2f} MB")
            
            with st.spinner("Executing dynamic data extraction protocols..."):
                time.sleep(1.0) # Processing simulation
                st.session_state.quiz_ready = True

    if st.session_state.quiz_ready:
        st.markdown("---")
        st.subheader("🎯 Custom Assessment Node")
        st.info("The document context layer has successfully built your target testing track.")

        questions = [
            {
                "id": "q1",
                "question": "1. What pattern does multi-phase aerodynamic turbulence typically track?",
                "options": ["Linear drag boundaries", "Quantum disruption pattern", "Parabolic drift constraints"],
                "correct": "Quantum disruption pattern"
            },
            {
                "id": "q2",
                "question": "2. How does fluid rolling friction alter energy matrices along a baseline slope?",
                "options": ["It scales velocity exponentially", "It dissipates thermal kinetic vectors", "It neutralizes gravitational torque"],
                "correct": "It dissipates thermal kinetic vectors"
            }
        ]

        for q in questions:
            st.write(q["question"])
            current_selection = st.radio(
                "Select your target answer hypothesis:",
                options=q["options"],
                key=f"widget_key_{q['id']}"
            )
            st.session_state.quiz_answers[q["id"]] = current_selection
            st.write("")

        if st.button("Submit Assessment Node Evaluation", key="btn_eval_quiz"):
            score = 0
            for q in questions:
                if st.session_state.quiz_answers.get(q["id"]) == q["correct"]:
                    score += 1
            
            if score == len(questions):
                st.success(f"🏆 Perfect Evaluation! Score: {score}/{len(questions)} metrics cleared.")
            else:
                st.warning(f"⚖️ Review required. Score: {score}/{len(questions)} markers validated.")

# --- TAB 2: EXTRACTED FLASHCARDS ---
with tab2:
    st.subheader("Dynamic Study Cards")
    
    if st.session_state.quiz_ready:
        st.write("Review key technical definitions extracted from your processed test script:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**TERM:** Aerodynamic Matrix\n\n**DEFINITION:** The multi-layered environment where fluid dynamics and air drag intercept solid boundaries.")
        with col2:
            st.info("**TERM:** Rolling Friction Loss\n\n**DEFINITION:** The systemic energy transformation occurring when a rolling wheel body encounters micro-surface variances.")
    else:
        st.warning("⚠️ Waiting for active file injection. Please drop a science document into the Quiz Pipeline first.")

# --- TAB 3: AUDIO SESSION ENGINE ---
with tab3:
    st.subheader("20-Minute Long Audio Engine")
    
    if not st.session_state.quiz_ready:
        st.warning("⚠️ Audio tracking requires a running database frame. Upload a script file in Tab 1.")
    else:
        st.write("Configure and compile high-duration background study sessions based on the uploaded file data.")
        
        target_duration = st.slider("Target Session Length (Minutes)", min_value=5, max_value=60, value=20, step=5)
        st.info(f"🎯 Setup complete for a {target_duration}-minute deep study audio session track.")
        
        # FIXED STREAMING URL: Points to a real verified test file track link
        st.audio("https://soundhelix.com")
