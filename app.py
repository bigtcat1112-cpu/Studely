import streamlit as st
import os
from podcast import generate_long_podcast

# Set up page config and custom aesthetic styling
st.set_page_config(page_title="Studley App", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #F5F2EB;
        color: #4A4A4A;
    }
    div[data-testid="stSidebar"] {
        background-color: #EAE6DF;
    }
    .stButton>button {
        background-color: #D1C9BC;
        color: #4A4A4A;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #C2B8A8;
        color: #4A4A4A;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Studley Learning Workspace")

# Step 1: Hard-Stop File Upload Gate
st.sidebar.header("📁 Study Material")
uploaded_file = st.sidebar.file_uploader(
    "Upload a text file to unlock your flashcards, quiz, and podcast:", 
    type=["txt"],
    key="studley_file_uploader"
)

if uploaded_file is None:
    st.info("👋 Welcome! Please upload a dash-separated text note file in the sidebar to get started.")
    st.stop()

# Cache file content to prevent unnecessary re-reading on UI changes
@st.cache_data
def load_uploaded_data(file_obj):
    bytes_data = file_obj.read()
    return bytes_data.decode("utf-8")

raw_text = load_uploaded_data(uploaded_file)

# Parse content into structured items (assuming dash-separated formatting)
flashcards_data = []
for line in raw_text.splitlines():
    if "-" in line:
        parts = line.split("-", 1)
        term = parts[0].strip()
        definition = parts[1].strip()
        if term and definition:
            flashcards_data.append({"term": term, "definition": definition})

if not flashcards_data:
    st.warning("⚠️ The uploaded file doesn't seem to contain valid text formats. Please check your file layout.")
    st.stop()

# Initialize session states safely
if "flashcard_index" not in st.session_state:
    st.session_state.flashcard_index = 0
if "show_definition" not in st.session_state:
    st.session_state.show_definition = False
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "podcast_ready" not in st.session_state:
    st.session_state.podcast_ready = False
if "podcast_path" not in st.session_state:
    st.session_state.podcast_path = ""

# Step 2: Multi-tab navigation
tab1, tab2, tab3 = st.tabs(["📚 Flashcards", "📝 Quiz", "🎙️ Podcast Studio"])

# --- TAB 1: FLASHCARDS ---
with tab1:
    st.header("Interactive Flashcards")
    total_cards = len(flashcards_data)
    idx = st.session_state.flashcard_index

    # Display Card
    card_container = st.container(border=True)
    with card_container:
        st.markdown(f"**Card {idx + 1} of {total_cards}**")
        if not st.session_state.show_definition:
            st.subheader(f"🔍 Term: {flashcards_data[idx]['term']}")
        else:
            st.subheader(f"💡 Definition: {flashcards_data[idx]['definition']}")

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Previous", key="prev_card_btn"):
            st.session_state.flashcard_index = (idx - 1) % total_cards
            st.session_state.show_definition = False
            st.rerun()
    with col2:
        if st.button("🔄 Flip Card", key="flip_card_btn"):
            st.session_state.show_definition = not st.session_state.show_definition
            st.rerun()
    with col3:
        if st.button("Next ➡️", key="next_card_btn"):
            st.session_state.flashcard_index = (idx + 1) % total_cards
            st.session_state.show_definition = False
            st.rerun()

# --- TAB 2: QUIZ ---
with tab2:
    st.header("Knowledge Check Quiz")
    st.markdown("Test your memory based on your custom workspace notes!")
    
    # Generate simple multi-choice mockup based on data
    for i, item in enumerate(flashcards_data[:3]):  # Limit to first few items for demonstration
        st.markdown(f"**Question {i+1}: What is the definition of *'{item['term']}'*?**")
        options = [item['definition'], "An incorrect sample option A", "An incorrect sample option B"]
        
        # Keep choice consistent across re-renders with specific keys
        user_choice = st.radio("Select the correct answer:", options, key=f"quiz_q_{i}")
        if user_choice == item['definition']:
            st.success("🎯 Correct!")
        else:
            st.caption("Select an option above to test your skills.")

# --- TAB 3: PODCAST STUDIO ---
with tab3:
    st.header("Automated Deep-Dive Podcast")
    st.write("Generate and listen to an extended, comprehensive audio breakdown of your notes.")
    
    # Generation Button Triggers
    if st.button("🚀 Generate Goated Audio Experience", key="gen_podcast_btn"):
        with st.spinner("AI is rendering your audio into temporary server memory..."):
            # Call our separate module file logic
            audio_file_path = generate_long_podcast(flashcards_data)
            
            if audio_file_path and os.path.exists(audio_file_path):
                st.session_state.podcast_path = audio_file_path
                st.session_state.podcast_ready = True
                st.success("🎉 Temporary Audio Production Complete!")
            else:
                st.error("❌ Audio generation failed. Make sure your dependencies are active.")

    # Render working audio player if generation is successful
    if st.session_state.podcast_ready and st.session_state.podcast_path:
        st.write("---")
        st.subheader("📻 Now Playing: Complete Lesson Overview")
        
        # Read the file from hidden storage and load it directly to player
        if os.path.exists(st.session_state.podcast_path):
            with open(st.session_state.podcast_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
        else:
            st.error("The file has already been destroyed or cleaned up!")

        # SELF-DESTRUCT GATE BUTTON
        st.write(" ")
        if st.button("🗑️ Done Listening (Wipe File From Memory)", key="delete_audio_btn"):
            try:
                if os.path.exists(st.session_state.podcast_path):
                    os.remove(st.session_state.podcast_path) # Wipes file off server completely!
                
                # Reset Streamlit memory flags cleanly
                st.session_state.podcast_path = ""
                st.session_state.podcast_ready = False
                st.toast("🔥 Target file wiped and deleted cleanly!", icon="🧹")
                st.rerun()
            except Exception as e:
                st.error(f"Error executing cleanup sequence: {e}")
