import os
import streamlit as st
import time
import io
from gtts import gTTS

# Custom dark theme styling with beige-grey text and bright accents
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
        border: 2px solid #E6A23C !important;
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

# Keep the session data safe so it doesn't disappear when she changes tabs
if "custom_podcast_script" not in st.session_state:
    st.session_state.custom_podcast_script = None
if "custom_audio_data" not in st.session_state:
    st.session_state.custom_audio_data = None

def build_dynamic_script(topic, minutes, level):
    """
    Creates a dynamic script tailored to how simple she wants it 
    and adds more paragraphs depending on her chosen session time.
    """
    # 1. Adapt the wording based on her Simplification Level
    if level == "Super Simple (5th Grade Style)":
        explain_style = "Think of it like building blocks or a cool game: we break it down into easy, bite-sized steps so anyone can master it instantly."
        connector = "That makes total sense! Let's explain the next part with an easy real-world analogy."
    elif level == "Regular (Clear & Straightforward)":
        explain_style = "We are highlighting the main practical facts here, focusing on efficient concepts and smooth operations."
        connector = "Right, and keeping it straightforward helps us remember the core ideas without getting bogged down."
    else: # Advanced Deep-Dive
        explain_style = "We must analyze the structural mechanics, system boundaries, and optimization formulas driving this system."
        connector = "Precisely. Let's process the macro-level dependencies and study the advanced technical layout."

    # 2. Base conversational blocks
    intro = [
        ("Host 1 (Tristan)", f"Hey everyone, welcome back! Today we are tackling a cool topic: {topic}."),
        ("Host 2 (Co-Host)", f"That's right. And for this session, our main goal is to make sure we understand it inside and out. {explain_style}")
    ]
    
    outro = [
        ("Host 1 (Tristan)", f"That brings us to the end of our scheduled runtime block. This was awesome!"),
        ("Host 2 (Co-Host)", "Totally agree! Keep studying these blocks and you'll be an absolute expert. See you next time!")
    ]

    # 3. Dynamic content scaling based on requested minutes
    # More minutes = more detailed study sections generated inside the script loop
    study_topics = [
        "Getting Started & Core Rules",
        "How the Parts Connect Cleanly",
        "Secret Tips & Common Mistakes",
        "The Big Picture & Real-World Use",
        "Reviewing What We Learned",
        "Advanced Practice Goals"
    ]
    
    # Scale loops: 5 mins gets 1 section, 20 mins gets up to 5 sections
    sections_count = max(1, min(len(study_topics), int(minutes // 4)))
    
    middle_blocks = []
    for i in range(sections_count):
        section_name = study_topics[i]
        middle_blocks.extend([
            ("Host 1 (Tristan)", f"Let's move on to Section {i+1}: {section_name}. What is the most important takeaway here?"),
            ("Host 2 (Co-Host)", f"For {section_name}, the main trick is focusing on consistency. {connector}"),
            ("Host 1 (Tristan)", "Exactly! If you get this part right, everything else becomes way cleaner and easier to run.")
        ])

    return intro + middle_blocks + outro

def render_podcast_app():
    st.title("🎙️ Sis's Custom Podcast Creator")
    st.subheader("Design Your Perfect Audio Learning Session")
    
    # Text source fallback if app.py is empty
    source_text = st.session_state.get("workspace_file_content", "")
    if not source_text:
        source_text = st.text_area(
            "Enter study topic or notes below:",
            value="How to build an independent online business selling candles, soap, and automated mechanical blankets.",
            key="fallback_podcast_input"
        )
    else:
        st.info("📋 Successfully reading from your uploaded workspace document file!")

    st.write("---")
    st.subheader("⚙️ Customization Settings Panel")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Custom Length Setting
        session_minutes = st.slider(
            "🕒 Desired Audio Length (Minutes):",
            min_value=2,
            max_value=20,
            value=20, # Defaults to her favorite 20-minute length
            step=1,
            key="sis_podcast_minutes"
        )
        
    with col2:
        # Simplification Level Setting
        sim_level = st.selectbox(
            "🧠 Level of Simplification:",
            ["Super Simple (5th Grade Style)", "Regular (Clear & Straightforward)", "Advanced Deep-Dive"],
            index=0,
            key="sis_simplification"
        )
        
    with col3:
        # Voice Type Configuration
        voice_choice = st.selectbox(
            "🗣️ Co-Host Voice Accent:",
            ["British Studio Accent", "Australian Studio Accent", "Indian Studio Accent", "Standard American"],
            index=0,
            key="sis_voice_accent"
        )

    # Map the dropdown choices to gTTS Top-Level Domains (TLDs) for different sounds
    tld_map = {
        "British Studio Accent": "co.uk",
        "Australian Studio Accent": "com.au",
        "Indian Studio Accent": "co.in",
        "Standard American": "com"
    }
    selected_tld = tld_map[voice_choice]

    if st.button("🚀 Master & Generate Audio Show", key="trigger_sis_podcast"):
        with st.spinner("Analyzing rules and generating your custom script..."):
            
            script = build_dynamic_script(source_text[:150], session_minutes, sim_level)
            st.session_state.custom_podcast_script = script
            
            combined_audio = io.BytesIO()
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for index, (speaker, speech_text) in enumerate(script):
                status_text.text(f"Mixing Track {index + 1} of {len(script)} ({speaker})...")
                
                # Determine voice: Host 1 is Tristan (US), Host 2 uses her custom accent pick
                tld_to_use = "com" if "Tristan" in speaker else selected_tld
                
                tts = gTTS(text=speech_text, lang="en", tld=tld_to_use, slow=False)
                
                temp_segment = io.BytesIO()
                tts.write_to_fp(temp_segment)
                temp_segment.seek(0)
                
                # Append segment into final file memory buffer
                combined_audio.write(temp_segment.read())
                
                # Increment visual tracker
                progress_bar.progress((index + 1) / len(script))
                time.sleep(0.05)
                
            combined_audio.seek(0)
            st.session_state.custom_audio_data = combined_audio.getvalue()
            status_text.text("✨ Studio Mix Complete! Player Deck Initialized.")
            st.balloons()

    # Visual Output Rendering Gate
    if st.session_state.custom_podcast_script:
        st.write("---")
        st.subheader("🎧 Playback Deck & Script Display")
        
        if st.session_state.custom_audio_data:
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
