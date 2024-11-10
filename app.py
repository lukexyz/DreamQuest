import streamlit as st
from claudette import Claude
import os

# Set page config
st.set_page_config(
    page_title="Children's Story Generator",
    page_icon="📚",
    layout="centered"
)

# Initialize session state for the Claude client
if 'claude_client' not in st.session_state:
    st.session_state.claude_client = None

# Sidebar for API key input
with st.sidebar:
    api_key = st.text_input("Enter your Anthropic API Key", type="password")
    if api_key:
        st.session_state.claude_client = Claude(api_key)

# Main app title
st.title("📚 Children's Story Generator")

# Input fields
age = st.number_input("Child's Age", min_value=2, max_value=12, value=6)
story_length = st.selectbox(
    "Story Length",
    options=["Short (100 words)", "Medium (300 words)", "Long (500 words)"]
)

# Base prompt template
story_prompt = """You are a skilled children's story writer. Create an engaging, age-appropriate story 
that sparks imagination and includes a subtle moral lesson. The story should be entertaining 
and educational, using language suitable for the specified age group."""

# Generate button
if st.button("Generate Story"):
    if not st.session_state.claude_client:
        st.error("Please enter your API key in the sidebar first!")
    else:
        st.info("Story generation will be implemented in the next step...")