import streamlit as st 
import google.generativeai as genai
from dotenv import load_dotenv
import os 
import json 

# Initialize the environment
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configure the page settings
st.set_page_config(page_title="Gemini chat", layout="wide")

# Application title
st.title("Tsinghua No. 70 ChatAI: Learning Chinese Vocabulary")

# Create a function to handle chatbot responses
def generate_bot_response(user_input):
    try:
        # Create conversation history from session state
        conversations = [
            {"role": msg["role"], "parts": [msg["content"]]}
            for msg in st.session_state.chat_history 
        ] 
        
        # Add the user’s question to the conversations 
        conversations.append({"role": "user", "parts": [user_input]})
        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-2.0-flash")
        chat = model.start_chat(history=conversations)
        
        # Pass the user’s question to the model
        # response = model.generate_content(user_input)
        response = chat.send_message(user_input)
        
        return response.text
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"
    

# Function to save chat history to a JSON file
def save_chat_history():
    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.chat_history, f, ensure_ascii=False, indent=2)
        

# Function to load chat history from a JSON file
def load_chat_history():
    try:
        with open("chat_history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Initialize session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()
    
# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Create an input box for the user to enter a question
prompt = st.chat_input("Nhập câu hỏi của bạn...")

if prompt:
    # Save the user's question to the chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    
    # Display the user’s message
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Call generate_bot_response
    response = generate_bot_response(prompt) 
    
    # Display the chatbot’s response
    with st.chat_message("assistant"):
        st.markdown(response)
        
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Save the chat history
    save_chat_history()
    
# Button to clear chat history
if st.button("Xóa lịch sử chat"):
    st.session_state.chat_history = []
    if os.path.exists("chat_history.json"):
        os.remove("chat_history.json")
    st.rerun()

