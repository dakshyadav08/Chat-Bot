import os

from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu

from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_response,
                            gemini_pro_vision_response,)

# Initialize working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Friday",
    page_icon="💀",
    layout="centered",
)

# Sidebar menu
with st.sidebar:
    selected = option_menu('Friday',
                           ['ChatBot',
                            'Image Captioning',
                            'Ask me anything'],
                           menu_icon='robot', icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
                           default_index=0
                           )

# Initialize session state variables
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None  # Placeholder for chat session

def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# ChatBot page
if selected == 'ChatBot':
    model = load_gemini_pro_model()

    if st.session_state.chat_session is None:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("💬 ChatBot")

    # Display chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt = st.chat_input("Ask Gemini-Pro...")
    if user_prompt:
        with st.spinner("Thinking..."):
            st.chat_message("user").markdown(user_prompt)
            gemini_response = st.session_state.chat_session.send_message(user_prompt)

        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Image Captioning page
if selected == "Image Captioning":
    st.title("📷 Snap Narrate")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        if st.button("Generate Caption"):
            image = Image.open(uploaded_image)
            
            col1, col2 = st.columns(2)

            with col1:
                resized_img = image.resize((800, 500))
                st.image(resized_img)

            default_prompt = "write a short caption for this image"

            with st.spinner("Generating caption..."):
                caption = gemini_pro_vision_response(default_prompt, image)

            with col2:
                st.info(caption)
    else:
        st.warning("Please upload an image to proceed.")

# Ask Me Anything page
if selected == "Ask me anything":
    st.title("🤙 Ask Me Anything")

    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if user_prompt.strip():
        if st.button("Get Response"):
            with st.spinner("Thinking..."):
                response = gemini_pro_response(user_prompt)
                st.markdown(response)
    else:
        st.warning("Please enter a question to get a response.")
