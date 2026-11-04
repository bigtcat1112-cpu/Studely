import streamlit as st
import os
from podcast import generate_long_podcast
from audio_factory import vaporize_target_audio_file

st.set_page_config(page_title="Studley Premium Workspace", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F7F5F0; color: #3A3A3A; }
    div[data-testid="stSidebar"] { background-color: #EDEAE4; }
    .stButton>button { background-color: #D3CBC0; color: #2F2F2F; border-radius: 12px; font-weight: bold; }
    .card-box { background-color: #FFFFFF; border: 1px solid #E5E2DA; border-radius: 16px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.02); }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Studley Learning Workspace")
st.subheader("Quantum Automated Study Dashboard")

st.sidebar.header("📁 Material Channel")
uploaded_file = st.sidebar.file_uploader("Select dash-separated .txt file:", type=["txt"], key="studley_file_uploader")

if uploaded_file is None:
    st.info("👋 System Standby. Please load a study text document in the sidebar.")
    st.stop()

raw_text = uploaded_file.read().decode("utf-8")
flashcards_data =

for line in raw_text.splitlines():
    if "-" in line:
        parts = line.split("-", 1)
        term = parts.strip()
        definition = parts.strip()
        if term and definition:
            flashcards_data.append({"term": term, "definition": definition})

if not flashcards_data:
    st.warning("⚠️ Formatting Warning: Ensure lines contain a dash character.")
    st.stop()

if "flashcard_index" not in st.session_state: st.session_state.flashcard_index = 0
if "show_definition" not in st.session_state: st.session_state.show_definition = False
if "podcast_ready" not in st.session_state: st.session_state.podcast_ready = False
if "podcast_path" not in st.session_state: st.session_state.podcast_path = ""

tab1, tab2, tab3 = st.tabs(["📚 Flashcards", "📝 Quiz Center", "🎙️ Podcast Lounge"])

# --- FLASHCARDS ---
with tab1:
    st.header("Interactive Visual Flashcards")
    idx = st.session_state.flashcard_index
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    if not st.session_state.show_definition:
        st.markdown(f"<h3>🔍 Concept:</h3><h1>{flashcards_data[idx]['term']}</h1>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h3>💡 Definition:</h3><h2>{flashcards_data[idx]['definition']}</h2>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⬅️ Back"):
            st.session_state.flashcard_index = (idx - 1) % len(flashcards_data)
            st.session_state.show_definition = False
            st.rerun()
    with c2:
        if st.button("🔄 Flip"):
            st.session_state.show_definition = not st.session_state.show_definition
            st.rerun()
    with c3:
        if st.button("Next ➡️"):
            st.session_state.flashcard_index = (idx + 1) % len(flashcards_data)
            st.session_state.show_definition = False
            st.rerun()

# --- QUIZ CENTER ---
with tab2:
    st.header("Automated Multiple-Choice Quiz Engine")
    for i, item in enumerate(flashcards_data[:3]):
        st.markdown(f"<div class='card-box'><b>Question {i+1}: Identify the parameters for: {item['term']}</b>", unsafe_allow_html=True)
        ans = st.radio("Select answer:", [item['definition'], "Wrong config A", "Wrong config B"], key=f"qz_{i}")
        if ans == item['definition']: st.success("🎯 Correct!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- PODCAST LOUNGE ---
with tab3:
    st.header("🎙️ Automated Goated Deep-Dive Podcast Lounge")
    st.write("Click below to compile text scripts directly into an physical audio file track inside server memory.")
    
    if st.button("🚀 Initialize Factory Audio Conversion Engine", key="gen_podcast_btn"):
        with st.spinner("Factory Worker is compiling text scripts and generating physical MP3 data streams..."):
            physical_mp3 = generate_long_podcast(flashcards_data)
            if physical_mp3 and os.path.exists(physical_mp3):
                st.session_state.podcast_path = physical_mp3
                st.session_state.podcast_ready = True
                st.success("🎉 Audio File Rendered and Stored Successfully inside Scratchspace Memory!")
            else:
                st.error("Audio generation pipeline failed. Check engine tracks.")

    if st.session_state.podcast_ready and st.session_state.podcast_path:
        st.write("---")
        st.markdown("<div class='card-box' style='border-left: 5px solid #3E8E41;'>", unsafe_allow_html=True)
        st.subheader("📻 Live Audio Stream Feed")
        st.caption("Listening directly to physical server scratchspace paths.")
        
        # Read the file directly from the secure factory folder path
        if os.path.exists(st.session_state.podcast_path):
            with open(st.session_state.podcast_path, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
        else:
            st.error("The file tracker has been terminated.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write(" ")
        if st.button("🗑️ Done Listening (Execute Ghost-Mode File Wipe)"):
            # Call the specialized cleanup tool from our factory file worker
            vaporize_target_audio_file(st.session_state.podcast_path)
            
            # Flush session memory grids completely
            st.session_state.podcast_path = ""
            st.session_state.podcast_ready = False
            st.toast("🔥 Operation Complete: Audio file shredded completely from disk memory!", icon="🧹")
            st.rerun()
