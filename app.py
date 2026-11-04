import streamlit as st

# 1. Page Setup & Style Customization
st.set_page_config(page_title="Studley", page_icon="🃏", layout="centered")

# Custom styling matching your bright beige and gray aesthetic
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FDFBF7;
    }
    h1, h2, h3, p, label {
        color: #4A4A46 !important;
    }
    div[data-baseweb="input"], div[data-testid="stFileUploader"] {
        background-color: #F5F3EF !important;
        border: 1px solid #D3CFC9 !important;
        border-radius: 8px;
        padding: 10px;
    }
    div[data-baseweb="input"] input {
        color: #4A4A46 !important;
    }
    .stButton>button {
        background-color: #EFECE6;
        color: #4A4A46;
        border: 1px solid #D3CFC9;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #E6A23C;
        color: white;
        border-color: #E6A23C;
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
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🃏 Studley Workspace")
st.write("Welcome to your podcast quiz and study hub!")

# Initialize Session States if they don't exist yet
if "card_index" not in st.session_state:
    st.session_state.card_index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# --- SECTION 1: MANDATORY FILE UPLOADER ---
st.markdown("---")
st.header("📤 Upload Study Material")
st.write("Drop your study notes or text files here to unlock your workspace!")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "md"])

# Lock screen if file is missing
if uploaded_file is None:
    st.warning("🔒 Please upload a text file above to unlock your flashcards, quiz, and podcast audio.")
    
    with st.expander("💡 Quick Guide: How to format your text file"):
        st.write("Create a text file where each line has a term and definition separated by a dash `-`. For example:")
        st.code("What is the capital of Texas? - Austin\nWhat is 12 x 12? - 144", language="text")
    st.stop()

# --- FILE PROCESSOR (UNLOCKED) ---
file_contents = uploaded_file.read().decode("utf-8")
st.success("📝 File uploaded successfully! Workspace unlocked.")

flashcards_data = []

# Automatically parse lines containing a dash '-'
lines = file_contents.split("\n")
for line in lines:
    if "-" in line:
        parts = line.split("-", 1)
        flashcards_data.append({"front": parts[0].strip(), "back": parts[1].strip()})

# Fallback if no lines matched our formatting rule
if not flashcards_data:
    flashcards_data = [
        {"front": "No dash '-' found in your file.", "back": "Please edit your text file so questions and answers are split with a dash '-'!"}
    ]
    with st.expander("👀 View Uploaded Raw Notes"):
        st.text(file_contents)
else:
    st.info(f"✨ Automatically generated {len(flashcards_data)} custom flashcards from your file!")

# --- SECTION 2: FLASHCARDS ---
st.markdown("---")
st.header("📇 Flashcard Station")

if st.session_state.card_index >= len(flashcards_data):
    st.session_state.card_index = 0

current_card = flashcards_data[st.session_state.card_index]

if not st.session_state.show_answer:
    display_text = f"💡 **Question / Term:**\n\n### {current_card['front']}"
else:
    display_text = f"✅ **Answer / Definition:**\n\n### {current_card['back']}"

st.markdown(f'<div class="flashcard-box">{display_text}</div>', unsafe_allow_html=True)

# Layout buttons using exactly 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Flip Card"):
        st.session_state.show_answer = not st.session_state.show_answer
        st.rerun()

with col2:
    if st.button("➡️ Next Card"):
        st.session_state.card_index = (st.session_state.card_index + 1) % len(flashcards_data)
        st.session_state.show_answer = False
        st.rerun()

# --- SECTION 3: PODCAST QUIZ ---
st.markdown("---")
st.header("🎙️ Podcast Audio & Quiz")
st.write("Listen to your lesson audio below, then test your knowledge!")

st.audio("https://soundhelix.com")

st.subheader("📝 Quick Quiz Check")
st.write("According to your uploaded study materials, can you solve this concept test?")

quiz_choice = st.radio(
    "Choose your answer based on your notes:",
    ["Option A: The material is too complex", 
     "Option B: Focusing on making the product clean and easy to use first", 
     "Option C: Skipping file uploads entirely"],
    index=None
)

if st.button("Submit Answer"):
    if quiz_choice == "Option B: Focusing on making the product clean and easy to use first":
        st.success("🎯 Correct! Keeping it simple and clean is always the winning strategy.")
    elif quiz_choice is None:
        st.warning("Please select an answer choice first!")
    else:
        st.error("❌ Not quite! Try reading your uploaded file details again.")
