import streamlit as st
from gtts import gTTS
import boto3
from googletrans import Translator
import base64
import time

# Initialize translator
translator = Translator()

# AWS Polly Client
session = boto3.Session(
    aws_access_key_id='AKIA2KX4BJV2Z5HPPFPF',
    aws_secret_access_key='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',
    region_name='ap-south-1'
)
polly_client = session.client('polly')

# Streamlit UI Enhancements
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button {
        background-color: #008cba;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 12px;
        margin-top: 10px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #005f73;
    }
    .stAudio {
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #4a4a4a;'>🌟 Text Processing Tool 🌟</h1>", unsafe_allow_html=True)
st.subheader("Welcome to the Text Processing Tool! Convert text to speech or translate it into different languages.")

# Text Input
text_input = st.text_area("Enter Text", height=150, placeholder="Type or paste your text here...")

# Option: Generate Speech or Translate
user_action = st.radio("What would you like to do?", ['Generate Speech from Original Text', 'Translate Text and Generate Speech'])

# Conditional UI
if user_action == 'Translate Text and Generate Speech':
    lang_options = {
        "English": 'en', "Spanish": 'es', "French": 'fr', "German": 'de', "Hindi": 'hi'
    }
    lang_choice = st.selectbox("Select Language for Translation", list(lang_options.keys()))

    # Additional Option for Generating Speech
    generate_speech = st.radio("Would you like to generate speech from translated text?", ['Yes', 'No'])

# Voice Type Selection (Male/Female)
voice_type = st.selectbox("Select Voice", ['Male', 'Female'])

# Process Speech Generation
if st.button("Generate Speech"):
    if text_input:
        if user_action == 'Generate Speech from Original Text':
            # Directly generate speech from original text
            text_to_convert = text_input

        elif user_action == 'Translate Text and Generate Speech':
            # Translate the text
            translated = translator.translate(text_input, dest=lang_options[lang_choice])
            text_to_convert = translated.text

            # Show translation result
            st.write(f"**Translated Text:** {text_to_convert}")
            
            if generate_speech == 'No':
                # If 'No' is selected, do not generate speech, stop further processing
                st.markdown("<h3 style='text-align: center; color: #6c757d;'>Thank You for using our application! 😊</h3>", unsafe_allow_html=True)
                st.stop()  # Stop any further processing

        # If the user selected 'Yes', proceed to generate speech
        with st.spinner("Generating speech..."):
            time.sleep(1)

            # AWS Polly voice mapping
            voice_map = {
                'Male': 'Matthew',  # Choose an AWS male voice
                'Female': 'Joanna'  # Choose an AWS female voice
            }

            # Polly Speech Synthesis
            response = polly_client.synthesize_speech(
                Text=text_to_convert,
                OutputFormat='mp3',
                VoiceId=voice_map[voice_type]
            )

            audio_data = response['AudioStream'].read()

            # Save the audio file
            with open("output.mp3", "wb") as f:
                f.write(audio_data)

            st.success("Speech generation successful!")

            # Display Audio Player
            st.audio("output.mp3", format="audio/mp3")

            # Download Option
            b64_audio = base64.b64encode(audio_data).decode()
            download_link = f'<a href="data:file/mp3;base64,{b64_audio}" download="output.mp3">Download Audio as MP3</a>'
            st.markdown(download_link, unsafe_allow_html=True)

        # Display Thank You message after processing
        st.markdown("<h3 style='text-align: center; color: #6c757d;'>Thank You for using our application! 😊</h3>", unsafe_allow_html=True)

    else:
        st.error("Please enter some text to proceed.")

# Footer with Dark Mode Toggle
st.markdown("""
    <div style='text-align: center; padding-top: 20px;'>
    <small>🌙 Click <strong>Preferences</strong> in the Streamlit menu for Dark Mode.</small>
    </div>
""", unsafe_allow_html=True)

# Thank You Message at the End
st.markdown("""
    <hr>
    <h3 style='text-align: center; color: #6c757d;'>Thank You for using our application! 😊</h3>
    <p style='text-align: center;'>We hope this tool helps you with your text and speech processing needs. Feel free to reach out for feedback or support!</p>
    <hr>
""", unsafe_allow_html=True)
