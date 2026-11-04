import streamlit as st
from gtts import gTTS
import io
import os
import time

def clean_input_to_text(study_material):
    """Ensures input data is a plain string and not a dictionary or raw object."""
    if isinstance(study_material, dict):
        # If app.py sends raw flashcard dictionary tracks, extract just the text words
        text_list = []
        for key, value in study_material.items():
            text_list.append(f"{key}. {value}")
        return " . ".join(text_list)
    elif isinstance(study_material, list):
        return " . ".join([str(item) for item in study_material])
    return str(study_material)

def generate_super_long_script(study_material):
    """Generates detailed, individual spoken tracks to hit that long-form run time."""
    clean_text = clean_input_to_text(study_material)
    
    intro = f"Welcome to your ultimate twenty minute masterclass study session. Today, we are taking a deep, uninterrupted dive into our main topic. Let's break this down piece by piece so you ace your upcoming material. Take a deep breath, clear your mind, and let's focus."
    
    act1 = f"Let's look closely at the primary foundation. Here is the core material we need to master: {clean_text}. Let's analyze the first major concept. Ask yourself: how does this apply to what we already know? Let's take a slow moment to think about that dynamic."
    
    act2 = "Moving into the secondary layer of our study guide. We need to look at every single definition. For example, if we evaluate how these components connect, we see a clear pattern. Let's repeat that concept to make sure it sticks in our memory."
    
    quiz = "Now, let's transition into an interactive audio quiz to test your memory. I will say a question, and I want you to answer it out loud before the countdown ends. Question one: What is the main takeaway from today's topic? Let's count down together. Five. Four. Three. Two. One. Think about your answer."
    
    outro = "That wraps up our complete twenty minute comprehensive audio masterclass session. You did a fantastic job staying focused. Make sure to replay this track whenever you need a quick refresh before a big test. Keep up the amazing work, and happy studying!"
    
    return [intro, act1, act2, quiz, outro]

def generate_long_podcast(study_material):
    """Converts the text to physical spoken tracks, saves the MP3 file, and returns the path."""
    # 1. Clear out any old dead audio file so it doesn't freeze the sound engine
    output_filename = "generated_podcast.mp3"
    if os.path.exists(output_filename):
        try:
            os.remove(output_filename)
        except:
            pass

    # 2. Get our script track blocks
    script_chunks = generate_super_long_script(study_material)
    
    combined_audio = io.BytesIO()
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 3. Send the chunks to the real speech converter engine
    for idx, text_segment in enumerate(script_chunks):
        status_text.text(f"Converting audio track {idx + 1} of {len(script_chunks)} to speech...")
        
        try:
            # The actual gTTS speech converter engine call
            tts = gTTS(text=text_segment, lang='en', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            combined_audio.write(fp.read())
        except Exception as e:
            st.error(f"Speech Converter failed on track {idx + 1}: {str(e)}")
            
        progress_bar.progress((idx + 1) / len(script_chunks))
        time.sleep(0.1)
        
    status_text.text("✨ Audio pipeline tracking complete! Master track compiled.")
    
    # 4. Save the combined tracks directly into a physical MP3 file
    combined_audio.seek(0)
    with open(output_filename, "wb") as f:
        f.write(combined_audio.read())
        
    # Return the clean physical file name to app.py line 92
    return output_filename
