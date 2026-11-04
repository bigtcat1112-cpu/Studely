import streamlit as st
# Place this right under your title in app.py
st.header("📤 Upload Study Material")
st.write("Drop your study notes or text files here to load them into the workspace!")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "md"])

if uploaded_file is not None:
    # Read the file contents as text
    file_contents = uploaded_file.read().decode("utf-8")
    st.success("📝 File uploaded successfully! Ready to study.")
    
    # Optional: Display a small preview of what she uploaded
    with st.expander("👀 Preview Uploaded Text"):
        st.write(file_contents)

# 1. Page Setup & Style Customization
st.set_page_config(page_title="Studley", page_icon="🃏", layout="centered")

# Custom styling for text inputs and background matching your aesthetic
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FDFBF7;
    }
    h1, h2, h3, p, label {
        color: #4A4A46 !important;
    }
    div[data-baseweb="input"] {
        background-color: #F5F3EF !important;
        border: 1px solid #D3CFC9 !important;
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
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# Sample Data (Later we can link this to your Supabase tables!)
flashcards_data = [
    {"front": "What is the capital of Texas?", "back": "Austin"},
    {"front": "What does a beginner programmer build first?", "back": "A cool app like Studley!"},
    {"front": "What is 12 x 12?", "back": "144"}
]

# --- SECTION 1: FLASHCARDS ---
st.header("📇 Flashcard Station")

current_card = flashcards_data[st.session_state.card_index]

# Display Card Content
if not st.session_state.show_answer:
    display_text = f"💡 **Question:**\n\n### {current_card['front']}"
else:
    display_text = f"✅ **Answer:**\n\n### {current_card['back']}"

st.markdown(f'<div class="flashcard-box">{display_text}</div>', unsafe_allow_html=True)

# Card Action Buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔄 Flip Card"):
        st.session_state.show_answer = not st.session_state.show_answer
        st.rerun()

with col2:
    if st.button("➡️ Next Card"):
        st.session_state.card_index = (st.session_state.card_index + 1) % len(flashcards_data)
        st.session_state.show_answer = False
        st.rerun()


# --- SECTION 2: PODCAST QUIZ ---
st.markdown("---")
st.header("🎙️ Podcast Audio & Quiz")
st.write("Listen to the audio clip below, then test your knowledge!")

# Audio Player (You can plug in your Supabase audio file URL or an online file)
st.audio("https://soundhelix.com")

st.subheader("📝 Quick Quiz Check")
st.write("According to the audio lesson, which element is essential for launching a clean app?")

quiz_choice = st.radio(
    "Choose your answer:",
    ["Complex software code with hundreds of features", 
     "Focusing on making the product clean and easy to use first", 
     "Adding bright flashing neon animations"],
    index=None
)

if st.button("Submit Answer"):
    if quiz_choice == "Focusing on making the product clean and easy to use first":
        st.success("🎯 Correct! Keeping it simple and clean is always the winning strategy.")
    elif quiz_choice is None:
        st.warning("Please select an answer choice first!")
    else:
        st.error("❌ Not quite! Try listening again and think about what makes an empire app successful.")
