import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("RR_Healthcare_Bot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    # Add a system message to enforce guardrails
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a healthcare assistant specialized in providing general medical advice. "
                "Your responses should strictly focus on medical-related queries. "
                "If the user asks about non-medical topics, politely decline and remind them that you only handle medical-related questions. "
                "Do not provide diagnoses, prescriptions, or specific medical treatments—only offer general remedies and advice. "
                "Always encourage users to consult a licensed healthcare professional for personalized care."
            )
        }
    ]

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    if role != "system":  # Only display user and assistant messages, not the system message
        with st.chat_message(role):
            st.markdown(content)

# Collect user input for symptoms
user_input = st.chat_input("Describe your symptoms here...")

# Function to get a response from OpenAI with health advice
def get_response(prompt):
    # Include the system prompt and conversation history in the request
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": prompt}]
    )
    # Access the content directly as an attribute
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_prompt = f"User has reported the following symptoms: {user_input}. Provide a general remedy or advice."
    assistant_response = get_response(assistant_prompt)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
