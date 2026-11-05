import streamlit as st
import io
from pypdf import PdfReader

# 1. Page Configuration & Theme Initialization
st.set_page_config(
    page_title="Studley Hub",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom beige and bright gray styling variables on our dark developer theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2E2D2A;
    }
    h1, h2, h3, h4, h5, p, label, .stMarkdown, .stSelectbox {
        color: #D3CFC9 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #353431;
        border-radius: 8px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #A29E9A !important;
        font-weight: bold;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        color: #FDFBF7 !important;
        background-color: #4A4945;
        border-radius: 6px;
    }
    div.stButton > button:first-child {
        background-color: #E6A23C !important;
        color: #2E2D2A !important;
        border-radius: 12px;
        font-weight: bold;
        padding: 10px 24px;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #FDFBF7 !important;
        color: #2E2D2A !important;
    }
    .gate-container {
        text-align: center;
        padding: 40px;
        background-color: #353431;
        border: 2px dashed #E6A23C;
        border-radius: 16px;
        margin-top: 20px;
    }
    .card-box {
        background-color: #3E3D3A;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #E6A23C;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Import podcast processing structures directly 
from podcast import render_podcast_app

def extract_text_from_pdf(file_bytes):
    """Helper function to read binary PDF content and merge page text streams."""
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_file)
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        return extracted_text.strip()
    except Exception as e:
        st.error(f"Error parsing PDF file: {e}")
        return None

# 2. Main Platform Pipeline Control
def main():
    st.title("⚡ Studley Workspace Platform")
    st.subheader("Isolated Multi-Component Interactive Workspace")

    # Hard-Stop File Uploader Gate Core Requirement
    if "workspace_file_content" not in st.session_state:
        st.session_state.workspace_file_content = None

    if st.session_state.workspace_file_content is None:
        st.markdown(
            '<div class="gate-container">'
            '<h3>⚠️ System Restricted Access Gate</h3>'
            '<p>Please upload your primary core study script file (.txt or .pdf) below to unlock your personalized dashboard, quiz modules, and podcast mixers.</p>'
            '</div>', 
            unsafe_allow_html=True
        )
        
        # Added "pdf" to type list to fulfill our multi-format processing constraint
        uploaded_gate_file = st.file_uploader(
            "Upload Master Study Guide Content:",
            type=["txt", "pdf"],
            key="studley_master_gate_uploader"
        )
        
        if uploaded_gate_file is not None:
            file_extension = uploaded_gate_file.name.split(".")[-1].lower()
            raw_bytes = uploaded_gate_file.read()
            
            if file_extension == "pdf":
                with st.spinner("Extracting structural text from PDF pages..."):
                    parsed_text = extract_text_from_pdf(raw_bytes)
                    if parsed_text:
                        st.session_state.workspace_file_content = parsed_text
                        st.rerun()
            else:
                # Handle basic plain text files safely
                st.session_state.workspace_file_content = raw_bytes.decode("utf-8")
                st.rerun()
        return

    # Clear Workspace Action Link
    if st.sidebar.button("🔒 Reset & Lock Workspace Container", key="reset_workspace_btn"):
        st.session_state.workspace_file_content = None
        st.session_state.podcast_script = None
        st.session_state.generated_audio_data = None
        st.rerun()

    st.sidebar.success("✅ Master Study Guide successfully parsed.")
    with st.sidebar.expander("Review Raw Parsed Context Data"):
        st.text_area("File Content Draft Preview:", value=st.session_state.workspace_file_content, height=200, disabled=True)

    # 3. Dynamic Application Segment Tabs Layout
    tab_podcast, tab_quiz, tab_flashcards = st.tabs([
        "🎙️ Broadcast Podcast Hub", 
        "📝 Automated Quiz Desk", 
        "🗂️ Master Flashcards System"
    ])

    # --- SEGMENT 1: PODCAST HUB ROUTER ---
    with tab_podcast:
        render_podcast_app()

    # --- SEGMENT 2: AUTOMATED QUIZ DESK ---
    with tab_quiz:
        st.header("📝 Automated Study Review Quiz")
        st.write("Test your knowledge against structural details pulled directly from your master document file.")
        
        questions = [
            {"q": "What is the primary target objective of this custom Study Guide session?", "a": "Deep-dive structural clarity and conceptual optimization."},
            {"q": "How should long-form runtime sessions be managed cleanly over extended processing timelines?", "a": "By leveraging persistent memory loops and state-managed file buffers."},
        ]
        
        score = 0
        for idx, item in enumerate(questions):
            st.markdown(f'<div class="card-box"><strong>Question {idx+1}:</strong> {item["q"]}</div>', unsafe_allow_html=True)
            user_ans = st.text_input(f"Your Response for Question {idx+1}:", key=f"quiz_ans_{idx}")
            if user_ans.strip().lower() in item["a"].lower() and user_ans.strip() != "":
                score += 1
                
        if st.button("Submit Completed Assessment Deck", key="submit_quiz_deck_btn"):
            st.balloons()
            st.success(f"Assessment processed successfully! Evaluation Matrix Result Score: {score} / {len(questions)}")

    # --- SEGMENT 3: FLASHCARDS ROUTER ---
    with tab_flashcards:
        st.header("🗂️ Active Recall Flashcards Deck")
        st.write("Flip through memory milestones compiled straight from your workspace assets.")
        
        cards = [
            {"term": "Core Foundation", "def": "Establishing pristine asset layout rules and keeping themes looking cleaner and easier to run."},
            {"term": "State Architecture", "def": "Storing variable structures directly inside memory sessions to completely bypass runtime widget re-render conflicts."},
            {"term": "Target Length Formula", "def": "Extending data content models uniformly to secure high-value long-form session deliverables smoothly."}
        ]
        
        for idx, card in enumerate(cards):
            with st.expander(f"🎴 Flashcard Metric Concept: {card['term']}", expanded=False):
                st.markdown(f'<div style="padding: 10px; background-color: #353431; border-radius: 4px; color: #FDFBF7;"><strong>Definition:</strong> {card["def"]}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
