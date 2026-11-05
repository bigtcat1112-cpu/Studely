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

def build_dynamic_script(topic, minutes, level):
    """
    Builds an extensive conversational script matrix.
    Uses runtime text multipliers to scale length up seamlessly 
    for full 20-minute audio timelines.
    """
    if level == "Super Simple (5th Grade Style)":
        style_clause = "We're going to break this down using super easy examples, almost like building blocks or a video game tutorial!"
        host2_response = "Perfect! Let's keep it simple and skip all the confusing tech jargon."
    elif level == "Regular (Clear & Straightforward)":
        style_clause = "We will go through the direct operational guide step-by-step to understand the standard layout rules."
        host2_response = "Sounds good, let's keep it clear and focus purely on how things function."
    else:
        style_clause = "We must systematically analyze the deep underlying algorithms, design architectures, and database relationships."
        host2_response = "Excellent. We will isolate individual component variables and review the data matrix."

    script_blocks = [
        ("Host 1 (Tristan)", f"Hey everyone, welcome back! Today we have an exciting long-form study stream about: {topic}."),
        ("Host 2 (Co-Host)", f"That's right! Tristan, I am excited for this one. {style_clause}"),
        ("Host 1 (Tristan)", f"Me too! {host2_response} Let's dive straight into the foundational rules.")
    ]

    sub_modules = [
        "Core Concepts & Baseline Setup Rules",
        "Connecting the Moving Parts & Database Flow",
        "Common Mistakes to Completely Avoid",
        "Secret Tips for Faster Workflow Mastery",
        "Reviewing the Big Picture Applications",
        "Advanced Optimization & Next Steps"
    ]

    # Target text multiplier logic loops to secure extensive reading content
    loop_multiplier = max(1, int(minutes // 3))

    for iteration in range(loop_multiplier):
        for index, sub in enumerate(sub_modules):
            script_blocks.extend([
                ("Host 1 (Tristan)", f"Let's check out our next key segment: {sub}, section batch number {iteration + 1}."),
                ("Host 2 (Co-Host)", f"Regarding {sub}, the main thing to remember is staying consistent with your practice loops."),
                ("Host 1 (Tristan)", f"Exactly. If you get that core part down, managing the rest of this workspace layout gets much easier.")
            ])

    script_blocks.extend([
        ("Host 1 (Tristan)", "Wow, we have covered an incredible amount of information over this session length block."),
        ("Host 2 (Co-Host)", "Absolutely! Remember to review this audio file whenever you need a quick memory refresher. See you next time!"),
        ("Host 1 (Tristan)", "Thanks for hanging out. Stream closed, keep building!")
    ])

    return script_blocks

def render_podcast_app():
    st.title("🎙️ Sis's Custom Podcast Creator")
    st.subheader("Design Your Perfect Audio Learning Session")
    
    source_text = st.session_state.get("workspace_file_content", "")
    if not source_text:
        source_text = st.text_area(
            "Enter study topic or notes below:",
            value="Building an independent online store to sell custom candles, high-quality blankets, and soaps.",
            key="fallback_podcast_input"
        )
    else:
        st.success("📋 Successfully reading raw text data from your uploaded document container.")

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
        with st.spinner("Processing custom audio tracks... This may take a moment for longer sessions."):
            
            script = build_dynamic_script(source_text[:200], session_minutes, sim_level)
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
