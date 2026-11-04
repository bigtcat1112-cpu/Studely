import streamlit as st
import os
from podcast import generate_long_podcast

# Configure advanced page viewport matrix
st.set_page_config(
    page_title="Studley Premium Workspace", 
    page_icon="🎓", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom High-End Interface Theme Matrix
st.markdown("""
    <style>
    .stApp {
        background-color: #F7F5F0;
        color: #3A3A3A;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    div[data-testid="stSidebar"] {
        background-color: #EDEAE4;
        border-right: 1px solid #DCD9D2;
    }
    .stButton>button {
        background-color: #D3CBC0;
        color: #2F2F2F;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #C5BCB0;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #E5E2DA;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Studley Learning Workspace")
st.subheader("Advanced Automated Study Dashboard")

# --- SIDEBAR CONTROL UNIT ---
st.sidebar.header("📁 Material Ingestion Channel")
st.sidebar.write("Load your raw study documents below to boot up the workspace engines.")

uploaded_file = st.sidebar.file_uploader(
    "Select dash-separated .txt file:", 
    type=["txt"],
    key="studley_file_uploader"
)

if uploaded_file is None:
    st.info("👋 System Standby. Please feed a study text document into the side panel uploader matrix to initialize components.")
    st.stop()

@st.cache_data
def load_uploaded_data(file_obj):
    return file_obj.read().decode("utf-8")

raw_text = load_uploaded_data(uploaded_file)
flashcards_data = []

# Parse text streams safely
for line in raw_text.splitlines():
    if "-" in line:
        parts = line.split("-", 1)
        term = parts[0].strip()
        definition = parts[1].strip()
        if term and definition:
            flashcards_data.append({"term": term, "definition": definition})

if not flashcards_data:
    st.warning("⚠️ Formatting Warning: The document structure submitted could not be read cleanly. Ensure lines contain a dash character.")
    st.stop()

# State Vectors Synchronization
if "flashcard_index" not in st.session_state:
    st.session_state.flashcard_index = 0
if "show_definition" not in st.session_state:
    st.session_state.show_definition = False
if "podcast_ready" not in st.session_state:
    st.session_state.podcast_ready = False
if "podcast_path" not in st.session_state:
    st.session_state.podcast_path = ""
if "active_stream_url" not in st.session_state:
    st.session_state.active_stream_url = ""
if "active_category" not in st.session_state:
    st.session_state.active_category = ""

# Layout Workspace Tabs
tab1, tab2, tab3 = st.tabs(["📚 Flashcard Studio", "📝 Evaluation Center", "🎙️ Long-Form Podcast Lounge"])

# --- TAB 1: FLASHCARD STUDIO ---
with tab1:
    st.header("Interactive Visual Flashcards")
    total_cards = len(flashcards_data)
    idx = st.session_state.flashcard_index
    
    st.markdown(f"<div class='card-box'>", unsafe_allow_html=True)
    st.caption(f"Asset Index Track: Item {idx + 1} of {total_cards}")
    
    if not st.session_state.show_definition:
        st.markdown(f"<h3>🔍 Concept Key:</h3><h1 style='color:#2E5B88;'>{flashcards_data[idx]['term']}</h1>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h3>💡 Content Definition:</h3><h2 style='color:#3E8E41;'>{flashcards_data[idx]['definition']}</h2>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Backtrack Item"):
            st.session_state.flashcard_index = (idx - 1) % total_cards
            st.session_state.show_definition = False
            st.rerun()
    with col2:
        if st.button("🔄 Invert Card View"):
            st.session_state.show_definition = not st.session_state.show_definition
            st.rerun()
    with col3:
        if st.button("Advance Item ➡️"):
            st.session_state.flashcard_index = (idx + 1) % total_cards
            st.session_state.show_definition = False
            st.rerun()

# --- TAB 2: EVALUATION CENTER ---
with tab2:
    st.header("Automated Multiple-Choice Quiz Engine")
    st.write("Verifying deep contextual comprehension tracks below:")
    
    for i, item in enumerate(flashcards_data[:3]):
        st.markdown(f"<div class='card-box'><b>Objective {i+1}: Examine the criteria definitions and identify the matching parameter for: <i style='color:#2E5B88;'>{item['term']}</i></b>", unsafe_allow_html=True)
        options = [item['definition'], "Alternative incorrect structural configuration Alpha.", "Alternative incorrect structural configuration Beta."]
        
        user_choice = st.radio("Select verified answer vector:", options, key=f"quiz_premium_q_{i}")
        if user_choice == item['definition']:
            st.success("🎯 Evaluation parameter validated successfully! Correct.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: GHOST FACTORY PODCAST LOUNGE ---
with tab3:
    st.header("🎙️ Automated Goated Deep-Dive Podcast Lounge")
    st.write("Initialize the high-fidelity cloud streaming blueprint down below to compile your lesson audio tracks.")
    
    if st.button("🚀 Initialize Goated Audio Production Engine", key="gen_podcast_btn"):
        with st.spinner("AI Engine is compiling background tracks and allocating temporary asset files inside server cache data channels..."):
            audio_file_path = generate_long_podcast(flashcards_data)
            
            if audio_file_path and os.path.exists(audio_file_path):
                st.session_state.podcast_path = audio_file_path
                
                # Parse layout vectors from secure ghost file
                parsed_configs = {}
                with open(audio_file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if ":" in line:
                            k, v = line.strip().split(":", 1)
                            parsed_configs[k] = v
                
                st.session_state.active_stream_url = parsed_configs.get("URL", "")
                st.session_state.active_category = parsed_configs.get("CATEGORY", "Premium")
                st.session_state.podcast_ready = True
                st.success("🎉 Production Engine Deployed and Synchronized Successfully!")
            else:
                st.error("Audio generation pipeline failed. Internal data buffer exception.")

    if st.session_state.podcast_ready and st.session_state.podcast_path:
        st.write("---")
        st.markdown(f"<div class='card-box' style='border-left: 5px solid #2E5B88;'>", unsafe_allow_html=True)
        st.subheader(f"📻 Now Playing: Complete Lesson Master Track")
        st.write(f"**Sound Profile Variant:** High-Definition `{st.session_state.active_category.upper()}` Focus Wave")
        st.caption("Custom synthesized study wave streaming securely through isolated CDN conduits.")
        
        # Deploy high-fidelity audio stream player
        if st.session_state.active_stream_url:
            st.audio(st.session_state.active_stream_url, format="audio/mp3")
        else:
            st.error("Streaming link configuration array is empty.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write(" ")
        if st.button("🗑️ Done Listening (Execute Ghost-Mode File Wipe)"):
            if os.path.exists(st.session_state.podcast_path):
                try:
                    os.remove(st.session_state.podcast_path)
                except Exception as e:
                    pass
            # Clear configuration states completely
            st.session_state.podcast_path = ""
            st.session_state.active_stream_url = ""
            st.session_state.active_category = ""
            st.session_state.podcast_ready = False
            st.toast("🔥 Operation Complete: Hidden tracking files vaporized successfully!", icon="🧹")
            st.rerun()
