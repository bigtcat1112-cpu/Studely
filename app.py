import streamlit as st
import random
from io import BytesIO
from gtts import gTTS

# MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Studley AI - Dynamic Lecture Hub",
    page_icon="🎙️",
    layout="wide"
)

# --- CUSTOM BEIGE & GRAY CSS STYLING ---
st.markdown("""
    <style>
    .main .block-container { max-width: 1200px; padding-top: 2rem; }
    
    body {
        color: #2E2D2A;
    }
    
    /* Button Custom styling */
    div.stButton > button:first-child {
        background-color: #2E2D2A; 
        color: #FDFBF7; 
        border: 1px solid #D3CFC9;
        border-radius: 6px; 
        font-weight: bold; 
        width: 100%;
    }
    
    /* Text Input Background Customizations */
    div[data-baseweb="textarea"] textarea {
        background-color: #FDFBF7 !important;
        color: #2E2D2A !important;
    }
    
    div.stAudio { margin-bottom: 2rem; }
    
    /* Flashcard presentation block */
    .flashcard-box {
        background-color: #FDFBF7;
        border: 2px solid #D3CFC9;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        font-size: 1.2rem;
        color: #2E2D2A;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
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
parsed_cards = []
lines = [line.strip() for line in st.session_state.raw_text_data.split("\n") if len(line.strip()) > 5]

for line in lines:
    if ":" in line:
        term, definition = line.split(":", 1)
        parsed_cards.append({"front": term.strip(), "back": definition.strip()})
    else:
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
        
        if idx >= total_cards:
            idx = 0
            st.session_state.flashcard_index = 0
            
        current_card = parsed_cards[idx]
        st.write(f"Card {idx + 1} of {total_cards}")
        
        flip = st.toggle("Flip Card", key=f"flip_toggle_{idx}")
        
        if not flip:
            st.markdown(f'<div class="flashcard-box"><b>Concept:</b><br><br>{current_card["front"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="flashcard-box" style="border-color: #2E2D2A;"><b>Definition / Application:</b><br><br>{current_card["back"]}</div>', unsafe_allow_html=True)
            
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
    
    # DYNAMIC AI PODCAST AUDIO INGESTION LAYER
    if st.session_state.processing_complete and st.session_state.raw_text_data.strip():
        try:
            # --- CONVERSATIONAL SCRIPT GENERATOR ---
            # Automatically wraps raw inputs into an explanatory podcast script format
            podcast_script = "Hello, and welcome to your personalized Studley review track. "
            podcast_script += f"Today we are breaking down a layout containing {len(parsed_cards)} foundational items. "
            
            for index, card in enumerate(parsed_cards):
                podcast_script += f"Let's look at key concept number {index + 1}: {card['front']}. "
                podcast_script += f"To explain this simply, it means: {card['back']}. Take a moment to think about how this fits into your learning goals. "
                
            podcast_script += "That concludes our explanation segment for these structural updates. Let's move over to the concept check below to test your memory!"
            
            # Converts the generated conversational script into audio
            sound_buffer = BytesIO()
            tts_engine = gTTS(text=podcast_script, lang='en', slow=False)
            tts_engine.write_to_fp(sound_buffer)
            
            # Displays script preview text so users can read along
            with st.expander("📖 View Podcast Narrator Script"):
                st.write(podcast_script)
            
            # Feeds generated binary audio data frame into the live player component
            st.audio(sound_buffer.getvalue(), format="audio/mp3")
            st.success("🔊 AI Podcast narration generated successfully based on current inputs!")
        except Exception as audio_err:
            st.error(f"Failed to generate custom audio track: {str(audio_err)}")
    else:
        st.info("📢 Awaiting text payload input in the sidebar to generate a custom podcast lecture track.")
        
    st.markdown("---")
    st.subheader("📝 Automated Comprehensive Concept Check")
    
    if st.session_state.processing_complete and len(parsed_cards) >= 1:
        st.write("Evaluate your custom generated content questions below:")
        
        quiz_target = parsed_cards[st.session_state.flashcard_index % len(parsed_cards)]
        
        correct_answer = quiz_target["back"]
        wrong_option_1 = "This option represents an unverified system layout constraint parameter fallback."
        wrong_option_2 = "Disregard this execution stream statement block match criteria entirely."
        
        quiz_options = [correct_answer, wrong_option_1, wrong_option_2]
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
