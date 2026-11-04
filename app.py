import streamlit as st

# 1. Page Configuration & Strict Layout
st.set_page_config(page_title="Studley Hub", page_icon="🃏", layout="centered")

# Custom injection for a clean beige-gray theme that won't conflict with elements
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FDFBF7;
    }
    h1, h2, h3, p, label {
        color: #4A4A46 !important;
    }
    .flashcard-box {
        background-color: #F5F3EF;
        border: 2px solid #D3CFC9;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* Style file uploader to be cleanly clickable */
    div[data-testid="stFileUploader"] {
        background-color: #F5F3EF !important;
        border: 2px solid #D3CFC9 !important;
        border-radius: 8px;
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🃏 Studley Workspace")
st.write("The official family studio platform.")

# 2. Strict Session State Initialization
if "card_index" not in st.session_state:
    st.session_state.card_index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# --- SECTION 1: MANDATORY UPLOADER WALL ---
st.markdown("---")
st.header("📤 Step 1: Upload Study Notes")
st.write("Drop your text notes file below to compile your custom workspace.")

# Wrapped file uploader with a unique key to prevent module fetching issues
uploaded_file = st.file_uploader(
    label="Select a file from your computer (.txt or .md)",
    type=["txt", "md"],
    key="studley_file_uploader_core"
)

# Hard stop check if file is empty
if uploaded_file is None:
    st.warning("🔒 System Locked: Please upload a text file above to generate your sister's layout.")
    st.stop()

# --- SECTION 2: FILE DATA PROCESSOR ---
# If code reaches here, file definitely exists. Let's process it safely.
try:
    file_contents = uploaded_file.read().decode("utf-8")
    lines = file_contents.split("\n")
    
    parsed_flashcards = []
    for line in lines:
        if "-" in line:
            parts = line.split("-", 1)
            parsed_flashcards.append({
                "front": parts[0].strip(),
                "back": parts[1].strip()
            })
            
    # Fallback structure if formatting rules are missing dashes
    if not parsed_flashcards:
        parsed_flashcards = [
            {"front": "File loaded, but no dashes (-) found.", "back": "Format lines like: Term - Definition"}
        ]
except Exception as e:
    st.error("Error reading file compilation. Make sure it is plain text.")
    st.stop()

# --- SECTION 3: GENERATED FLASHCARDS ---
st.markdown("---")
st.header("📇 Step 2: Flashcard Station")
st.info(f"Loaded {len(parsed_flashcards)} items successfully.")

# Protect index overflow bounds
if st.session_state.card_index >= len(parsed_flashcards):
    st.session_state.card_index = 0

current_card = parsed_flashcards[st.session_state.card_index]

# View rendering logic
if not st.session_state.show_answer:
    display_text = f"💡 **Question / Term:**\n\n### {current_card['front']}"
else:
    display_text = f"✅ **Answer / Definition:**\n\n### {current_card['back']}"

st.markdown(f'<div class="flashcard-box">{display_text}</div>', unsafe_allow_html=True)

# Layout navigation split buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 Flip Card", key="flip_btn_action"):
        st.session_state.show_answer = not st.session_state.show_answer
        st.rerun()
with col2:
    if st.button("➡️ Next Card", key="next_btn_action"):
        st.session_state.card_index = (st.session_state.card_index + 1) % len(parsed_flashcards)
        st.session_state.show_answer = False
        st.rerun()

# --- SECTION 4: LESSON PODCAST & COMPILER QUIZ ---
st.markdown("---")
st.header("🎙️ Step 3: Podcast Audio & Quiz Hub")
st.write("Listen to the study breakdown track below:")

# Safe link track player
st.audio("https://soundhelix.com")

st.subheader("📝 Quick Quiz Check")
quiz_choice = st.radio(
    "Based on your lesson materials, identify the proper strategy:",
    ["A) Overcomplicating features instantly", 
     "B) Keeping product UI clean, simple, and easy to use first", 
     "C) Hiding code repositories entirely"],
    index=None,
    key="quiz_radio_selection"
)

if st.button("Submit Assessment", key="quiz_submit_btn"):
    if quiz_choice == "B) Keeping product UI clean, simple, and easy to use first":
        st.success("🎯 Correct! Building a clean user setup is key to growing an app empire.")
    elif quiz_choice is None:
        st.warning("Please choose a selection option first.")
    else:
        st.error("❌ Review your study notes text and attempt again.")
