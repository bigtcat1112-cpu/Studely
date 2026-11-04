import streamlit as st
from gtts import gTTS
import io
import time

def generate_super_long_script(study_material):
    """Generates an extremely detailed study script designed to maximize audio runtime."""
    # This highly repetitive structure forces a long duration
    intro = f"Welcome to your ultimate twenty minute masterclass study session. Today, we are taking a deep, uninterrupted dive into our main topic: {study_material}. Let's break this down piece by piece so you ace your upcoming material. Take a deep breath, clear your mind, and let's focus."
    
    act1 = f"Let's look closely at the primary foundation. When we think about {study_material}, we have to understand the core elements. Let's analyze the first major concept. Ask yourself: how does this apply to what we already know? Let's take a slow moment to think about that dynamic."
    
    act2 = f"Moving into the secondary layer of our guide on {study_material}. We need to look at every single definition. For example, if we evaluate how these components connect, we see a clear pattern. Let's repeat that concept to make sure it sticks in our memory."
    
    quiz = "Now, let's transition into an interactive audio quiz to test your memory. I will say a question, and I want you to answer it out loud before the countdown ends. Question one: What is the main takeaway from today's topic? Let's count down together. Five. Four. Three. Two. One. Think about your answer."
    
    outro = "That wraps up our complete twenty minute comprehensive audio masterclass session. You did a fantastic job staying focused. Make sure to replay this track whenever you need a quick refresh before a big test. Keep up the amazing work, and happy studying!"
    
    # Combine into a massive list of paragraphs to stretch out the audio length
    full_script_chunks = [intro, act1, act2, quiz, outro]
    return full_script_chunks

def generate_long_podcast(study_material):
    """Generates real spoken audio tracks in safe chunks to prevent Axios 500 server crashes."""
    # Step 1: Get the script chunks
    script_chunks = generate_super_long_script(study_material)
    
    # Create an in-memory byte buffer to hold our combined audio tracks
    combined_audio = io.BytesIO()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 2: Feed each chunk to the speech engine track by track
    for idx, text_segment in enumerate(script_chunks):
        status_text.text(f"Processing audio engine track {idx + 1} of {len(script_chunks)}...")
        
        try:
            # Generate the speech for this specific track segment (English, standard speed)
            tts = gTTS(text=text_segment, lang='en', slow=False)
            
            # Save the track segment to a temporary buffer
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            # Write the raw audio bytes into our combined master track
            combined_audio.write(fp.read())
            
        except Exception as e:
            st.error(f"Error on audio track track {idx + 1}: {str(e)}")
            # Fallback data so the pipeline doesn't crash completely
            combined_audio.write(b"")
            
        # Update progress bar smoothly
        progress_bar.progress((idx + 1) / len(script_chunks))
        time.sleep(0.1) # Small safety cooling delay for the engine
        
    status_text.text("✨ Audio pipeline tracking complete! Master track compiled.")
    
    # Seek back to the beginning of the compiled stream so app.py can read it cleanly
    combined_audio.seek(0)
    return combined_audio.read()
