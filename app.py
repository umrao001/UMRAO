import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
from google import genai

# ---------------- ENV ----------------
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("GOOGLE_API_KEY not found in .env")
    st.stop()

# ---------------- GEMINI CLIENT ----------------
client = genai.Client(
    api_key=API_KEY,
    http_options={"api_version": "v1alpha"}
)

MODEL_NAME = "gemini-2.5-flash"

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- GEMINI RESPONSE ----------------
def get_gemini_response(prompt, image=None):
    try:
        if image:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[prompt, image]
            )
        else:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
        return response.text
    except Exception as e:
        return f"Error: {e}"

# ---------------- UI ----------------
st.set_page_config(page_title="Gemini Multimodal Chatbot", layout="centered")
st.title("🤖 Gemini Multimodal Chatbot")
st.caption(f"Model: `{MODEL_NAME}`")

# Display chat history
for msg in st.session_state.chat_history:
    role = "You" if msg["role"] == "user" else "Gemini"
    st.markdown(f"**{role}:** {msg['text']}")
    if msg.get("image"):
        st.image(msg["image"], width=300)

# User input
user_input = st.text_input("Ask something (optional)")

# Image upload
uploaded_file = st.file_uploader(
    "Upload an image (optional)",
    type=["jpg", "jpeg", "png"]
)

image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Send button
if st.button("Send"):
    if not user_input and not image:
        st.warning("Please enter a message or upload an image.")
    else:
        prompt = user_input if user_input else "Describe this image"

        # Save user message
        st.session_state.chat_history.append({
            "role": "user",
            "text": prompt,
            "image": image
        })

        # Get Gemini response
        reply = get_gemini_response(prompt, image)

        # Save Gemini response
        st.session_state.chat_history.append({
            "role": "model",
            "text": reply
        })

        st.rerun()

# Clear chat
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
