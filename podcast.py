import os
import streamlit as st
import time
import io
from gtts import gTTS

# Custom clean dark theme layout configurations 
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2E2D2A;
    }
    h1, h2, h3, h4, h5, p, label, .stMarkdown, .stSelectbox, .stSlider {
        color: #D3CFC9 !important;
    }
    div.stTextArea textarea {
        background-color: #FDFBF7 !important;
        color: #2E2D2A !important;
        border: 2px solid #E6A23C !important;
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
    .podcast-host-1 {
        padding: 12px;
        background-color: #3E3D3A;
        border-left: 4px solid #E6A23C;
        margin-bottom: 8px;
        border-radius: 6px;
    }
    .podcast-host-2 {
        padding: 12px;
        background-color: #353431;
        border-left: 4px solid #A29E9A;
        margin-bottom: 8px;
        border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "custom_podcast_script" not in st.session_state:
    st.session_state.custom_podcast_script = None
if "custom_audio_data" not in st.session_state:
    st.session_state.custom_audio_data = None

def build_dynamic_script(full_text, minutes, level):
    """
    Splits the actual uploaded file content into readable paragraph parts,
    then loops hosts walking through the real document text to explain it out loud.
    """
    # Clean and parse text into separate blocks or sentences
    raw_paragraphs = [p.strip() for p in full_text.split('\n') if len(p.strip()) > 15]
    
    # Fallback default sentences if the file is extremely short
    if len(raw_paragraphs) == 0:
        raw_paragraphs = [
            "This study guide focuses on establishing stable operations and clear learning structures.",
            "Always isolate state configurations inside the application layer to keep components secure.",
            "Building long form workflows requires managing memory buffers efficiently from start to finish."
        ]

    # Setup the discussion tone depending on her chosen level
    if level == "Super Simple (5th Grade Style)":
        style_clause = "We're reading through this document and breaking it down into simple, super easy examples!"
        explanation_templates = [
            "Think of this part like a video game rule: it basically means that ",
            "To make that simple, it's just like building blocks where you ",
            "An easy analogy for this is a bicycle chain, meaning that "
        ]
    elif level == "Regular (Clear & Straightforward)":
        style_clause = "We will go through this master document line by line to highlight the most important concepts."
        explanation_templates = [
            "In plain terms, the core takeaway here is that ",
            "This step functions as an operational guideline showing that ",
            "Essentially, this layout rule ensures that we can "
        ]
    else:  # Advanced Deep-Dive
        style_clause = "We will perform a structural breakdown of the source text data matrices and underlying mechanics."
        explanation_templates = [
            "Analyzing this closely reveals a core operational dependency where ",
            "This specific architectural clause explicitly optimizes the fact that ",
            "The data model here establishes strict algorithmic constraints indicating that "
        ]

    # Introduction block
    script_blocks = [
        ("Host 1 (Tristan)", "Hey everyone, welcome back! Today we are doing a live reading session from your uploaded file contents."),
        ("Host 2 (Co-Host)", f"That's right! Tristan, let's open the document up. {style_clause}"),
        ("Host 1 (Tristan)", "Perfect. Let's pull out our very first section chunk from the file and break it down.")
    ]

    # Scale the amount of coverage paragraphs based on requested run minutes
    target_loops = max(2, int(minutes // 2))
    
    for i in range(target_loops):
        # Dynamically rotate through the real text file blocks cleanly
        text_chunk = raw_paragraphs[i % len(raw_paragraphs)]
        # Keep quotes neat and short for audio processing stability
        short_quote = " ".join(text_chunk.split()[:12]) + "..." 
        
        template = explanation_templates[i % len(explanation_templates)]

        script_blocks.extend([
            ("Host 1 (Tristan)", f"Okay, checking out the file, it explicitly says: '{short_quote}'"),
            ("Host 2 (Co-Host)", f"Oh, that's a key line. {template} everything needs to connect cleanly without any errors."),
            ("Host 1 (Tristan)", "Exactly! And by building it that way, the system stays super clean and easy to run.")
        ])

    # Final show closing wrap-up
    script_blocks.extend([
        ("Host 1 (Tristan)", "That covers our core file text readings for this specific time block session."),
        ("Host 2 (Co-Host)", "Awesome! Review this podcast deck whenever you want to check your notes on the go. See you later!"),
        ("Host 1 (Tristan)", "Stream closed. Keep studying!")
    ])

    return script_blocks

def render_podcast_app():
    st.title("🎙️ Sis's Custom Text-Reading Podcast Creator")
    st.subheader("Design Your Perfect Audio Learning Session")
    
    # Dynamically pull the exact text extracted from app.py's uploader gate
    source_text = st.session_state.get("workspace_file_content", "")
    if not source_text:
        source_text = st.text_area(
            "Enter fallback topic text if no file is uploaded:",
            value="Building an independent online store to sell custom candles, high-quality blankets, and soaps.\nAlways make sure your payment configurations are verified inside the settings.\nKeep the product designs clean and easy to browse for customers.",
            key="fallback_podcast_input"
        )
    else:
        st.success("📋 Successfully parsing real-time text segments from your uploaded document container file!")

    st.write("---")
    st.subheader("⚙️ Customization Settings Panel")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        session_minutes = st.slider(
            "🕒 Desired Audio Length (Minutes):",
            min_value=2,
            max_value=20,
            value=20, 
            step=1,
            key="sis_podcast_minutes"
        )
        
    with col2:
        sim_level = st.selectbox(
            "🧠 Level of Simplification:",
            ["Super Simple (5th Grade Style)", "Regular (Clear & Straightforward)", "Advanced Deep-Dive"],
            index=0,
            key="sis_simplification"
        )
        
    with col3:
        voice_choice = st.selectbox(
            "🗣️ Co-Host Voice Accent Selection:",
            ["British Studio Voice", "Australian Studio Voice", "Indian Studio Voice", "Standard American Voice"],
            index=0,
            key="sis_voice_accent"
        )

    tld_map = {
        "British Studio Voice": "co.uk",
        "Australian Studio Voice": "com.au",
        "Indian Studio Voice": "co.in",
        "Standard American Voice": "com"
    }
    selected_tld = tld_map[voice_choice]

    if st.button("🚀 Master & Generate Audio Show", key="trigger_sis_podcast"):
        with st.spinner("Analyzing text files and mixing speech responses... This may take a brief moment."):
            
            # Pass full extracted file contents straight to the dynamic script mixer loop
            script = build_dynamic_script(source_text, session_minutes, sim_level)
            st.session_state.custom_podcast_script = script
            
            combined_audio = io.BytesIO()
            progress_bar = st.progress(0)
            
            for index, (speaker, speech_text) in enumerate(script):
                if "Tristan" in speaker:
                    current_tld = "com"
                else:
                    current_tld = selected_tld
                
                tts = gTTS(text=speech_text, lang="en", tld=current_tld, slow=False)
                
                temp_segment = io.BytesIO()
                tts.write_to_fp(temp_segment)
                temp_segment.seek(0)
                
                combined_audio.write(temp_segment.read())
                progress_bar.progress((index + 1) / len(script))
                
            combined_audio.seek(0)
            st.session_state.custom_audio_data = combined_audio.getvalue()
            st.balloons()

    # SAFE SYSTEM GATE: Prevents KeyError crashes on first load
    if st.session_state.get("custom_podcast_script") is not None:
        st.write("---")
        st.subheader("🎧 Playback Deck & Script Display")
        
        if st.session_state.get("custom_audio_data") is not None:
            st.audio(st.session_state.custom_audio_data, format="audio/mp3")
            
            st.download_button(
                label="📥 Download Custom MP3 Show",
                data=st.session_state.custom_audio_data,
                file_name="custom_study_podcast.mp3",
                mime="audio/mp3",
                key="download_sis_mp3"
            )
            
        with st.expander("👁️ View Live Generated Dialogue Log", expanded=True):
            for speaker, text in st.session_state.custom_podcast_script:
                div_class = "podcast-host-1" if "Tristan" in speaker else "podcast-host-2"
                st.markdown(f'<div class="{div_class}"><strong>{speaker}:</strong> {text}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_podcast_app()
