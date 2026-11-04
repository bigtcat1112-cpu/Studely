import streamlit as st
import random

# MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Studley AI - Dynamic Lecture Hub",
    page_icon="🎙️",
    layout="wide"
)

# --- CUSTOM CSS STYLING ---
st.markdown("""
    <style>
    .main .block-container { max-width: 1200px; padding-top: 2rem; }
    div.stButton > button:first-child {
        background-color: #FF4B4B; color: white; border-radius: 6px; font-weight: bold; width: 100%;
    }
    div.stAudio { margin-bottom: 2rem; }
    .flashcard-box {
        background-color: #f7f5f0;
        border: 2px solid #d3cfc9;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        font-size: 1.2rem;
        color: #2e2d2a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "raw_text_data" not in st.session_state:
    st.session_state.raw_text_data = ""
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False
if "flashcard_index" not in st.session_state:
    st.session_state.flashcard_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None

# --- APP LAYOUT HEADER ---
st.title("🎙️ Studley Dynamic Lecture & Assessment Hub")
st.caption("Automated Content Parsing Environment | Isolated State Modules")

# --- TEXT MANIPULATION ENGINE ---
with st.sidebar:
    st.subheader("📁 Input Payload Ingestion")
    
    upload_method = st.radio(
        "Select Data Ingestion Method:",
        ["Direct Text Input Vector", "File Stream Vector"],
        key="ingestion_method_selector"
    )
    
    if upload_method == "Direct Text Input Vector":
        user_input_payload = st.text_area(
            "Paste Lecture Notes / Content Here:",
            height=250,
            placeholder="Format ideas:\nConcept 1: Definition here\nConcept 2: Details here",
            key="fallback_text_ingestion_buffer"
        )
        if st.button("Generate Workspace Assets", key="process_text_stream_trigger"):
            if user_input_payload.strip():
                st.session_state.raw_text_data = user_input_payload
                st.session_state.processing_complete = True
                st.session_state.flashcard_index = 0
                st.session_state.quiz_score = None
                st.success("✅ Content ingested successfully!")
            else:
                st.error("❌ Buffer Empty: Please insert a valid payload string first.")
                
    else:
        uploaded_file = st.file_uploader(
            "Upload System Log / Document Payload", 
            type=["txt", "log", "md"],
            key="isolated_platform_file_uploader"
        )
        if uploaded_file is not None:
            string_data = uploaded_file.read().decode("utf-8")
            st.session_state.raw_text_data = string_data
            st.session_state.processing_complete = True
            st.session_state.flashcard_index = 0
            st.session_state.quiz_score = None
            st.success("✅ File payload safely ingested.")

# --- DATA PARSING THREAD ENGINE ---
# Automatically builds flashcards/quiz choices based on text lines
parsed_cards = []
lines = [line.strip() for line in st.session_state.raw_text_data.split("\n") if len(line.strip()) > 5]

for line in lines:
    if ":" in line:
        term, definition = line.split(":", 1)
        parsed_cards.append({"front": term.strip(), "back": definition.strip()})
    else:
        # Fallback split if no colon is present
        words = line.split()
        if len(words) > 4:
            term = " ".join(words[:2])
            definition = " ".join(words[2:])
            parsed_cards.append({"front": term, "back": definition})

# --- NAVIGATION LAYER ---
tab_hub, tab_flashcards, tab_quiz, tab_raw = st.tabs([
    "🎯 Core Dashboard", 
    "📇 Flashcards",
    "📝 Assessment Center", 
    "📁 Raw Stream Logs"
])

# TAB 1: CORE DASHBOARD
with tab_hub:
    st.header("⚡ Core Operational Space")
    if st.session_state.processing_complete and parsed_cards:
        st.info("🚀 Content successfully parsed into dynamic study modules. Use the tabs above to explore your flashcards and assessments!")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total Words Ingested", value=len(st.session_state.raw_text_data.split()))
        with col2:
            st.metric(label="Generated Study Assets", value=len(parsed_cards))
    elif st.session_state.processing_complete and not parsed_cards:
        st.warning("⚠️ Text detected, but it's too short or improperly structured to generate cards. Try writing structured sentences or using 'Term: Definition' patterns.")
    else:
        st.warning("💤 Awaiting text input. Populate the sidebar input vector to unlock your automated lecture assets.")

# TAB 2: DYNAMIC FLASHCARDS
with tab_flashcards:
    st.header("📇 Automated Flashcard System")
    if st.session_state.processing_complete and parsed_cards:
        idx = st.session_state.flashcard_index
        total_cards = len(parsed_cards)
        
        # Keep index safely inside array bounds
        if idx >= total_cards:
            idx = 0
            st.session_state.flashcard_index = 0
            
        current_card = parsed_cards[idx]
        
        st.write(f"Card {idx + 1} of {total_cards}")
        
        # Flip Toggle UI
        flip = st.toggle("Flip Card", key=f"flip_toggle_{idx}")
        
        if not flip:
            st.markdown(f'<div class="flashcard-box"><b>Concept:</b><br><br>{current_card["front"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="flashcard-box" style="border-color: #FF4B4B;"><b>Definition / Application:</b><br><br>{current_card["back"]}</div>', unsafe_allow_html=True)
            
        # Navigation Buttons
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("⏮️ Previous Card") and idx > 0:
                st.session_state.flashcard_index -= 1
                st.rerun()
        with col_next:
            if st.button("Next Card ⏭️") and idx < total_cards - 1:
                st.session_state.flashcard_index += 1
                st.rerun()
    else:
        st.caption("No dynamic cards built yet. Add content in the sidebar.")

# TAB 3: LECTURE PODCAST HUB & ASSESSMENT
with tab_quiz:
    st.header("🎙️ Lecture Podcast Hub & Assessment")
    st.write("Play the direct streaming audio track tracking your structural updates, then verify performance matrices.")
    
    # Audio Player Execution Layer (Points directly to a clean, verifiable MP3 file)
    st.audio("https://soundhelix.com")
    st.markdown("---")
    
    st.subheader("📝 Automated Comprehensive Concept Check")
    
    if st.session_state.processing_complete and len(parsed_cards) >= 1:
        st.write("Evaluate your custom generated content questions below:")
        
        # Pick a target card based on the current deck tracking
        quiz_target = parsed_cards[st.session_state.flashcard_index % len(parsed_cards)]
        
        # Set up options dynamically
        correct_answer = quiz_target["back"]
        wrong_option_1 = "This option represents an unverified system layout constraint parameter fallback."
        wrong_option_2 = "Disregard this execution stream statement block match criteria entirely."
        
        quiz_options = [correct_answer, wrong_option_1, wrong_option_2]
        # Sort options cleanly so the correct choice isn't always option number one
        quiz_options.sort()
        
        quiz_selection = st.radio(
            label=f"Based on your processed data inputs, what best defines or applies to: '{quiz_target['front']}'?",
            options=quiz_options,
            index=None,
            key="production_grade_quiz_radio_matrix"
        )
        
        if st.button("Submit Assessment Processing Request", key="production_quiz_submit_trigger"):
            if quiz_selection is None:
                st.warning("Assessment input buffer empty. Choose an evaluation criteria option before processing.")
            elif quiz_selection == correct_answer:
                st.success("🎯 Evaluation: 100% Accurate. Keeping execution simple, clean, and accessible ensures scalable growth.")
            else:
                st.error("❌ Evaluation: Inaccurate Strategy Match. Re-read foundational system optimization metrics and try again.")
    else:
        st.caption("Awaiting dynamic quiz generation parameters. Add valid lecture notes in the sidebar to build your test.")

# TAB 4: RAW STREAM INSPECTION PANEL
with tab_raw:
    st.header("📁 Raw Stream Inspection Panel")
    st.write("Verify the string block exactly as ingested by the parsing thread engine array.")
    st.text_area(
        "Read-Only Log Stream Dump", 
        value=st.session_state.raw_text_data, 
        height=400, 
        disabled=True,
        key="read_only_logger_display"
    )
