import os
import shutil  # NEW
import streamlit as st
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from tempfile import NamedTemporaryFile
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tools import image_caption_tool, object_detection_tool, image_generation_tool, extract_text_tool, tavily_search
from dotenv import load_dotenv


## Load Environment Variables
load_dotenv()

# --- Dedicated workspaces (hidden folders) ---  
_TMP_DIR = ".tmp"
_GEN_DIR = ".gen"

def _ensure_workspace():  
    os.makedirs(_TMP_DIR, exist_ok=True)
    os.makedirs(_GEN_DIR, exist_ok=True)

_ensure_workspace()


# One-time init
if "uploader_token" not in st.session_state:
    st.session_state.uploader_token = 0


# -------- Reset function to clear generated files, temporary files and session state ---------

def reset_app():
    # 1) Remove working directories entirely
    for d in (_TMP_DIR, _GEN_DIR):
        try:
            if os.path.isdir(d):
                shutil.rmtree(d)
        except Exception:
            pass

    # 2) Recreate empty dirs
    _ensure_workspace()

    # 3) Clear widget/session state so uploader & app don’t respawn files
    st.session_state.pop("temp_path", None)
    st.session_state.uploader_token += 1
    #st.session_state.pop("model_provider", None)  # reset model choice 


# ----------------- Tools List -----------------

tools = [image_caption_tool, object_detection_tool, image_generation_tool, extract_text_tool, tavily_search]


# ------------------------- Page Config --------------------------
st.set_page_config(page_title="Pixel Dialogue", page_icon="🧠")
# -------------------------- Title --------------------------
st.title("🧠 Pixel Dialogue")
st.markdown("Chat with an Image using Langchain")




with st.sidebar:
    st.header("Settings")
    
    model_provider = st.radio(
        "Select Model Provider",
        ["GROQ", "Google"],
        key="model_provider"
    )

    st.button(
        "Reset", 
        type = "primary", 
        on_click = reset_app,
        width="stretch"
    )
    
if(model_provider == "GROQ"):
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
        
    llm = ChatGroq(
        model = "meta-llama/llama-4-scout-17b-16e-instruct",
        temperature = 0.5
    )

    agent = create_agent(
        model = llm,
        tools=tools,
        checkpointer = InMemorySaver()
    )
elif(model_provider == "Google"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
        
    llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash-lite",
        temperature = 0.5
    )

    agent = create_agent(
        model = llm,
        tools=tools,
        checkpointer = InMemorySaver()
    )


# Create config for the agent
config = {"configurable": {"thread_id": "test1"}}

system_message = SystemMessage(content="""
You are a helpful AI assistant with access to image tools. 
When a user provides a file path and asks a question, you MUST use the 
appropriate tool (like extract_text_tool or object_detection_tool) 
to get the information before answering. 
Do not explain how to use the tool; just use it.
""")

# upload file
file = st.file_uploader("", type=["jpeg", "jpg", "png"], key=f"uploaded_img_{st.session_state.uploader_token}")  # CHANGED: add key


if file:
    st.image(file, use_container_width=True)
    user_question = st.text_input('Ask a question about your image:')

    if 'temp_path' not in st.session_state:
        # Save the uploaded file inside ./.tmp/
        suffix = os.path.splitext(file.name)[1] or ".jpg"
        with NamedTemporaryFile(delete=False, suffix=suffix, dir=_TMP_DIR) as f:  # CHANGED: dir=_TMP_DIR
            f.write(file.getbuffer())
        st.session_state.temp_path = f.name

    image_path = st.session_state.temp_path

    if user_question and user_question != "":
        # Display the user's question immediately
        with st.chat_message("user"):
            st.write(user_question)

        with st.spinner(text="Thinking..."):
            # Run the agent
            response = agent.invoke(
                {"messages": [system_message, HumanMessage(content=f"{user_question}. Path: {image_path}")]}, 
                config=config
            )
            
            all_messages = response["messages"]
            
            # We want the last message that isn't empty
            # Usually, this is either the ToolMessage or the final AI summary
            display_msg = next((m.content for m in reversed(all_messages) if m.content.strip()), "I couldn't find an answer.")

            with st.chat_message("assistant"):
                st.write(display_msg)
            

            # Search for image paths in all tool messages and display them
            for msg in all_messages:
                if isinstance(msg, ToolMessage):
                    p = str(msg.content)
                    # Check if the tool output is a valid image file path
                    if os.path.exists(p) and p.lower().endswith(('.png', '.jpg', '.jpeg')):
                        st.image(p, caption="Generated Image")


# Examples
st.markdown("---")
st.markdown("### 💡Try these examples:")
col1, col2 = st.columns(2)
with col1:
    st.markdown("- Please describe this image")
    st.markdown("- What are the objects in this image?")
    st.markdown("- Please give me all the objects in the image, their bounding boxes and confidence scores")
    st.markdown("- Please extract text from this image")
with col2:
    st.markdown("- What is the caption of this image?")
    st.markdown("- Generate a image of black puppy sitting on green grass")
    st.markdown("- Please write 250 words long story involving the characters in the image")
