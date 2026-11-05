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
    Parses the file into full paragraphs, then sequences dialogue row blocks 
    using massive conversational padding strings to strictly maximize output length.
    """
    # Clean text and split precisely into a list of full standalone paragraphs
    raw_paragraphs = [p.strip() for p in full_text.split('\n\n') if len(p.strip()) > 30]
    if not raw_paragraphs:
        raw_paragraphs = [p.strip() for p in full_text.split('\n') if len(p.strip()) > 30]
        
    # Full default paragraphs fallback if the uploaded text source file is too short
    if len(raw_paragraphs) == 0:
        raw_paragraphs = [
            "Building an independent online business store requires clear target product rules. You must decide whether to manufacture items like high-quality blankets, organic custom candles, or specialty handcrafted soaps completely independently. Managing your setup parameters smoothly ensures a premium client checkout conversion timeline.",
            "Always make sure that backend system integrations are completely tested inside dashboard configurations before going live. Verifying API keys prevents hidden routing breakdowns and keeps processing streams fully optimized over runtime sessions. Keeping data containers isolated is critical to scaling operations cleanly.",
            "Long-form production architectures depend on stable memory handling loops from start to finish. If variable frameworks lack explicit unique widget keys, multi-tab system pipelines will hit re-render stutter errors. Maintaining structural clarity across development modules guarantees a premium user platform experience."
        ]

    # Adjust explanation frameworks and banter lengths based on the requested simplification level
    if level == "Super Simple (5th Grade Style)":
        style_clause = "We are diving through this file paragraph by paragraph and breaking everything down into awesome, easy-to-understand shortcuts!"
        commentary_pool = [
            "Wow, that is such a cool paragraph! Let's think about this like building blocks or a video game tutorial. Basically, what it's trying to show us is that everything needs to work together step-by-step. If you skip a single rule, the whole tower can tumble down, so keeping your parts organized is your secret superpower!",
            "That makes complete sense! Imagine you are riding a bike down a big hill—you need your gears and chain moving smoothly together without getting stuck. That is exactly what this section is talking about. It's telling us to keep things simple, clean, and completely fun so it's super easy to master.",
            "I love how that was written! It reminds me of setting up a giant Hot Wheels track loop. If the track connection points don't snap together perfectly, the toy cars fly off the rails. So the big takeaway here is to double-check your work and make sure every single piece is securely locked into place!"
        ]
    elif level == "Regular (Clear & Straightforward)":
        style_clause = "We will analyze this document page by page, reading full text blocks followed by clear, actionable summaries."
        commentary_pool = [
            "This is a vital paragraph to emphasize. In plain terms, the operational takeaway here focuses on workflow efficiency. You want to make sure your baseline framework functions reliably under standard conditions before adding more complex elements to the mix.",
            "Right, and looking closely at those specific lines, it outlines a clear blueprint for everyday management. By executing these procedural steps carefully, we completely eliminate common system bottlenecks and keep things working properly.",
            "Exactly. The structural rule defined in this segment ensures that all your data inputs align cleanly. Sticking to this straightforward method keeps your active workspace organized and easy to maintain over time."
        ]
    else:  # Advanced Deep-Dive
        style_clause = "We will execute a rigorous architectural parsing of individual text matrices and systemic data dependencies."
        commentary_pool = [
            "Analyzing the structural dimensions of this paragraph reveals a compelling operational pattern. The layout establishes algorithmic constraints that dictate how component dependencies interface across the primary application execution layer.",
            "Precisely. This technical block highlights a critical optimization vector. By implementing strict state isolation constraints here, we prevent runtime memory allocation overlaps and maintain pristine system stability.",
            "An excellent point. The macro-level variables detailed in this section suggest that all background pipeline calculations must map seamlessly to your primary database schema to ensure architectural consistency under load."
        ]

    # Introduction sequence
    script_blocks = [
        ("Host 1 (Tristan)", "Welcome back to the studio, everyone! Today we have an extensive, long-form master reading stream planned."),
        ("Host 2 (Co-Host)", f"That's right, Tristan! We are opening up the uploaded document file right now. {style_clause}"),
        ("Host 1 (Tristan)", "Perfect. Let's pull out our very first full paragraph from the source file and read it out loud.")
    ]

    # Calculate loops based on requested length (higher slider position = processes more paragraphs or loops deeper)
    target_sections = max(3, int(minutes // 2))
    
    for i in range(target_sections):
        # Pick one full, complete paragraph out of the file array sequentially
        current_paragraph = raw_paragraphs[i % len(raw_paragraphs)]
        commentary_text = commentary_pool[i % len(commentary_pool)]

        # Sequence 1: Tristan reads the exact full paragraph text chunk out loud
        script_blocks.append((
            "Host 1 (Tristan)", 
            f"Let's read our next full section text block from the file. It states: '{current_paragraph}'"
        ))
        
        # Sequence 2: Co-host immediately breaks down that exact paragraph with long-form padding conversation
        script_blocks.append((
            "Host 2 (Co-Host)", 
            f"Thanks for reading that full block, Tristan. Let's comment on that part immediately. {commentary_text} It really shows why this document matters."
        ))
        
        # Sequence 3: Tristan adds structural transition banter back to lengthen text weight smoothly
        script_blocks.append((
            "Host 1 (Tristan)", 
            f"Absolutely right! That explanation makes it totally clear. Let's advance right into the next complete paragraph section from our document file."
        ))

    # Outro wrap-up sequence
    script_blocks.extend([
        ("Host 1 (Tristan)", "And that officially brings us to the end of our deep text reading track block for today's session."),
        ("Host 2 (Co-Host)", "What an incredible study session! Make sure to save this custom audio file to your desktop player for easy review. See you next time!"),
        ("Host 1 (Tristan)", "Stream mastering complete. Catch you later, keep building!")
    ])

    return script_blocks

def render_podcast_app():
    st.title("🎙️ Sis's Long-Form Paragraph Podcast Creator")
    st.subheader("Design Your Perfect Audio Learning Session")
    
    # Read the text string seamlessly from the main app gate uploader state
    source_text = st.session_state.get("workspace_file_content", "")
    if not source_text:
        source_text = st.text_area(
            "Enter fallback topic text if no file is uploaded:",
            value="Building an independent online store to sell custom candles, high-quality blankets, and soaps.\n\nAlways make sure your payment configurations are verified inside the settings.\n\nKeep the product designs clean and easy to browse for customers.",
            key="fallback_podcast_input"
        )
    else:
        st.success("📋 Ready! Successfully reading full text paragraphs from your uploaded file container.")

    st.write("---")
    st.subheader("⚙️ Customization Settings Panel")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        session_minutes = st.slider(
            "🕒 Desired Audio Length (Minutes):",
            min_value=2,
            max_value=20,
            value=20, # Defaults to her favorite 20-minute timeline length
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
        with st.spinner("Processing custom audio paragraphs... This may take a moment for long-form sessions."):
            
            # Send extracted raw text down to our padding-heavy generator loop
            script = build_dynamic_script(source_text, session_minutes, sim_level)
            st.session_state.custom_podcast_script = script
            
            combined_audio = io.BytesIO()
            progress_bar = st.progress(0)
            
            for index, (speaker, speech_text) in enumerate(script):
                if "Tristan" in speaker:
                    current_tld = "com"
                else:
                    current_tld = selected_tld
                
                # Render isolated text blocks to ensure voice accent modifications stick cleanly
                tts = gTTS(text=speech_text, lang="en", tld=current_tld, slow=False)
                
                temp_segment = io.BytesIO()
                tts.write_to_fp(temp_segment)
                temp_segment.seek(0)
                
                combined_audio.write(temp_segment.read())
                progress_bar.progress((index + 1) / len(script))
                
            combined_audio.seek(0)
            st.session_state.custom_audio_data = combined_audio.getvalue()
            st.balloons()

    # SAFE SYSTEM GATE: Prevents KeyError crashes on first page loads
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
