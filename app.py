import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import uuid

# Load environment variables (like GOOGLE_API_KEY)
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash") # No "models/" prefix needed for common models

# Set Streamlit page configuration
st.set_page_config(page_title="AquaSathi")
st.title("💧 AquaSathi – Clean Water & Sanitation Chatbot")
st.markdown("Your friendly AI guide for hygiene, safe water, and sanitation 💬", unsafe_allow_html=True)

# --- Initialize Session State Variables ---
if "messages" not in st.session_state:
    st.session_state.messages = []
# `last_user_prompt` will store the prompt for which "More Details" is relevant
if "last_user_prompt" not in st.session_state:
    st.session_state.last_user_prompt = ""
# `show_detailed_button` controls when the "More Details" button appears
if "show_detailed_button" not in st.session_state:
    st.session_state.show_detailed_button = False
# `scroll_anchor` for auto-scrolling to the bottom of the chat
if "scroll_anchor" not in st.session_state:
    st.session_state.scroll_anchor = str(uuid.uuid4())

# Add new session states for detailed answer (as per your snippet)
if "detailed_prompt" not in st.session_state:
    st.session_state.detailed_prompt = ""
if "detailed_answer" not in st.session_state:
    st.session_state.detailed_answer = ""


# --- Sidebar Content ---
with st.sidebar:
    st.header("💧 AquaSathi")
    st.markdown("AI assistant for clean water & sanitation awareness.")
    st.markdown("Ask about:\n- Water hygiene\n- Safe sanitation practices\n- Water conservation tips")
    st.markdown("Start chatting to get personalized advice and information!")

    # Show Clear Chat only if chat has started
    if st.session_state.messages:
        if st.button("🧹 Clear Chat"):
            st.session_state.messages.clear()
            st.session_state.last_user_prompt = "" # Clear this as well
            st.session_state.show_detailed_button = False # Hide the detailed button
            st.session_state.detailed_prompt = ""
            st.session_state.detailed_answer = ""
            st.session_state.scroll_anchor = str(uuid.uuid4()) # Generate new anchor on clear
            st.rerun()
    else:
        st.markdown("_(Start chatting to see more options)_")


# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# This will automatically be pinned to the bottom of the page
prompt = st.chat_input("Ask something about water, hygiene, or sanitation...")

if prompt:
    # 1. User submits a prompt
    # Store the prompt for potential detailed answer and hide previous detailed button
    st.session_state.last_user_prompt = prompt
    st.session_state.show_detailed_button = False # Hide old button if a new prompt comes

    # Display user message and add to history
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare chat history for Gemini (includes previous turns for context)
    # Gemini expects roles "user" and "model"
    formatted_history = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            formatted_history.append({"role": "user", "parts": [msg["content"]]})
        elif msg["role"] == "assistant":
            formatted_history.append({"role": "model", "parts": [msg["content"]]})

    # 2. Generate and display short response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."): # Show spinner while generating
            full_response = ""
            try:
                # Use generation config for short response
                short_prompt = f"Answer this question in 2-3 simple sentences:\n{st.session_state.last_user_prompt}"

                response_stream = model.generate_content(
                    [{"role": "user", "parts": [short_prompt]}],
                    stream=True,
                    generation_config=genai.GenerationConfig(
                        max_output_tokens=150,
                        temperature=0.4,
                        top_p=0.9
                    )
                )
                for chunk in response_stream:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌") # Blinking cursor
                message_placeholder.markdown(full_response) # Final message
            except Exception as e:
                full_response = f"❌ Gemini API error for short response: {e}. Please check your key or connection."
                message_placeholder.markdown(full_response)

    # Append short response to messages (using 'assistant' role for consistency in session state)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Set flag to show "More Details" button for this new short answer
    st.session_state.show_detailed_button = True

    # Rerun to ensure all new messages are displayed and the "More Details" button appears
    st.rerun()

# --- "More Details" Button Logic ---
# This block runs on every rerun. It only displays the button if `show_detailed_button` is True.
if st.session_state.show_detailed_button and st.session_state.last_user_prompt:
    # Use a unique key for the button to prevent Streamlit issues
    more_details_button_key = f"more_details_btn_{st.session_state.last_user_prompt}"

    if st.button("🔍 More Details", key=more_details_button_key):
        # When "More Details" is clicked, generate detailed response
        st.session_state.show_detailed_button = False # Hide the button immediately after click

        # Prepare history including all prior turns + the instruction for detailed answer
        detailed_formatted_history = []
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                detailed_formatted_history.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                detailed_formatted_history.append({"role": "model", "parts": [msg["content"]]})

        # Add the instruction for a detailed answer based on the last prompt
        detailed_formatted_history.append({"role": "user", "parts": [f"Provide a comprehensive, detailed, and informative answer for the original query about: {st.session_state.last_user_prompt}"]})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Generating detailed response..."): # Show spinner
                full_detailed_response = ""
                try:
                    detailed_response_stream = model.generate_content(
                        detailed_formatted_history,
                        stream=True,
                        generation_config=genai.GenerationConfig(
                            temperature=0.6, # Slightly more creative for detailed answers, but still factual
                            top_p=0.9
                        )
                    )
                    for chunk in detailed_response_stream:
                        full_detailed_response += chunk.text
                        message_placeholder.markdown(full_detailed_response + "▌") # Blinking cursor
                    message_placeholder.markdown(full_detailed_response) # Final message
                except Exception as e:
                    full_detailed_response = f"❌ Error generating detailed response: {e}"
                    message_placeholder.markdown(full_detailed_response)

        # Display the detailed answer immediately
        # st.chat_message("assistant").markdown(detailed_text) # This is now handled by streaming
        # Append detailed answer to messages
        st.session_state.messages.append({"role": "assistant", "content": full_detailed_response})

        # Clear last_user_prompt so that this detailed answer is considered "done"
        st.session_state.last_user_prompt = ""

        st.rerun() # Rerun to update chat display and remove the button