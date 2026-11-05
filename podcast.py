import os
import streamlit as st
import time
import io
from gtts import gTTS

# Apply custom dark container background with bright beige-grey UI contrasts
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2E2D2A;
    }
    h1, h2, h3, h4, h5, p, label, .stMarkdown, .stSelectbox {
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
    }
    div.stButton > button:first-child:hover {
        background-color: #FDFBF7 !important;
        border: 2px solid #E6A23C !important;
    }
    .podcast-host-1 {
        padding: 10px;
        background-color: #3E3D3A;
        border-left: 4px solid #E6A23C;
        margin-bottom: 8px;
        border-radius: 4px;
    }
    .podcast-host-2 {
        padding: 10px;
        background-color: #353431;
        border-left: 4px solid #A29E9A;
        margin-bottom: 8px;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Session States to prevent playback resets on rerenders
if "podcast_script" not in st.session_state:
    st.session_state.podcast_script = None
if "generated_audio_data" not in st.session_state:
    st.session_state.generated_audio_data = None

def generate_podcast_script(topic, style):
    """
    Generates a structured, multi-segment co-host outline sequence 
    to create long-form dynamic conversational text profiles.
    """
    # Simulated structure to build extensive 20-minute target audio transcripts
    intro_segments = [
        ("Host 1 (Tristan)", f"Welcome back to Studley Audio Hub! Today, we are breaking down a highly requested topic: {topic}."),
        ("Host 2 (AI)", "That's right! We wanted to present this layout clearly, exploring every angle without leaving anything behind."),
    ]
    
    deep_dive_segments = []
    sections = ["Foundational Concepts", "Core Mechanics", "Advanced Real-World Strategies", "Future Outlooks"]
    
    for idx, section in enumerate(sections):
        deep_dive_segments.extend([
            ("Host 1 (Tristan)", f"Let's move into our next major focus area: {section}. Why does this layer matter so much?"),
            ("Host 2 (AI)", f"Excellent point. With {section}, the main goal is clarity. We analyze how parts interact cleanly."),
            ("Host 1 (Tristan)", f"Exactly, and when managing this over longer periods, consistency becomes your secret weapon."),
            ("Host 2 (AI)", "Which brings us to the operational aspect. Let's dig deeper into the examples mentioned in the guide.")
        ])
        
    outro_segments = [
        ("Host 1 (Tristan)", "This has been an incredibly long and detailed breakdown session. Any final thoughts for our listeners?"),
        ("Host 2 (AI)", "Take it one step at a time! Review the audio blocks, practice the templates, and stay tuned for the next drop."),
        ("Host 1 (Tristan)", "Thanks for joining us on Studley. See you in the next session!")
    ]
    
    return intro_segments + deep_dive_segments + outro_segments

def render_podcast_app():
    st.title("🎙️ Studley Podcast Show Producer")
    st.subheader("Bespoke Multi-Speaker Conversational Audio Suite")
    
    # User Input Panel
    topic = st.text_area(
        "Enter your focal study topic, notes, or raw script data:",
        value="Rocket engine design principles, combustion velocity, and chemical propulsion matrices.",
        height=120,
        key="podcast_topic_input"
    )
    
    podcast_style = st.selectbox(
        "Select Podcast Conversation Formula:",
        ["Educational / Deep-Dive Study", "Energetic Tech Breakdown", "Casual Professional Dialogue"],
        key="podcast_style_select"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        playback_pace = st.checkbox("Optimize text intervals for natural pacing", value=True, key="pace_check")
    
    if st.button("Compile & Master Podcast App", key="run_podcast_engine"):
        if not topic.strip():
            st.warning("Please provide context text or a topic to generate content.")
            return
            
        with st.spinner("Processing topic and script architectures..."):
            script = generate_podcast_script(topic, podcast_style)
            st.session_state.podcast_script = script
            
            # Using in-memory bytes loops directly to prevent OS blockages
            combined_audio = io.BytesIO()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for index, (speaker, speech_text) in enumerate(script):
                status_text.text(f"Mastering Audio Block {index + 1} of {len(script)} ({speaker})...")
                
                # Alternate slightly between standard speech tones to emulate dual speakers
                lang_modifier = 'en'
                tld_modifier = 'com' if "Tristan" in speaker else 'co.uk'
                
                tts = gTTS(text=speech_text, lang=lang_modifier, tld=tld_modifier, slow=False)
                
                # Fetch bytes chunk directly
                temp_segment = io.BytesIO()
                tts.write_to_fp(temp_segment)
                temp_segment.seek(0)
                
                # Write current segment into the global engine container
                combined_audio.write(temp_segment.read())
                
                # Update visual progress tracker
                progress_bar.progress((index + 1) / len(script))
                time.sleep(0.1)
                
            combined_audio.seek(0)
            st.session_state.generated_audio_data = combined_audio.getvalue()
            status_text.text("✨ Mixing completed! Studio file initialized.")
            
    # Persistent View Rendering Gate
    if st.session_state.podcast_script:
        st.write("---")
        st.subheader("🎧 Live Master Deck & Script Roll")
        
        # Audio Player Component using clean memory pointers
        if st.session_state.generated_audio_data:
            st.audio(st.session_state.generated_audio_data, format="audio/mp3")
            
            st.download_button(
                label="📥 Export Podcast MP3 Broadcast",
                data=st.session_state.generated_audio_data,
                file_name="studley_podcast_broadcast.mp3",
                mime="audio/mp3",
                key="persist_download_btn"
            )
            
        # Display the visual running dialogue log
        with st.expander("View Interactive Prompt Script Outline", expanded=True):
            for speaker, text in st.session_state.podcast_script:
                div_class = "podcast-host-1" if "Tristan" in speaker else "podcast-host-2"
                st.markdown(f'<div class="{div_class}"><strong>{speaker}:</strong> {text}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_podcast_app()
