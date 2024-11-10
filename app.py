import streamlit as st
from claudette import *
import os

# Set page config
st.set_page_config(
    page_title="Story Time",
    page_icon="📚",
    layout="centered"
)

# Custom CSS for the first letter styling
st.markdown("""
    <style>
    .first-letter {
        float: left;
        font-family: 'Georgia', serif;
        font-size: 75px;
        line-height: 60px;
        padding-top: 4px;
        padding-right: 8px;
        padding-left: 3px;
    }
    .prompt-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize client and chat
api_key = os.environ.get('ANTHROPIC_API_KEY')
if api_key:
    client = Client(api_key)
    model = models[1]  # Using claude-3-sonnet
    chat = Chat(model, 
        sp="You are a skilled children's story writer who creates engaging, age-appropriate stories.")
else:
    st.error("Please set ANTHROPIC_API_KEY in your environment variables!")

# Main app title
st.title("📚 Children's Story Generator")

# Create two columns
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Story Settings")
    # Input fields
    age = st.number_input("Child's Age", min_value=2, max_value=12, value=6)
    story_length = st.selectbox(
        "Story Length",
        options=["Short (100 words)", "Medium (300 words)", "Long (500 words)"]
    )
    generate_button = st.button("Generate Story")

# Get word count from selection
word_count = int(story_length.split()[1].strip("()"))

# Story prompt
story_prompt = f"""Create an engaging story suitable for a {age}-year-old child. 
The story should be approximately {word_count} words long, include a subtle moral lesson,
and be both entertaining and educational.
Only return the story itself, no title or additional commentary."""

with right_col:
    st.subheader("Current Prompt")
    st.markdown(f"""<div class="prompt-box">{story_prompt}</div>""", unsafe_allow_html=True)

# Generate story
if generate_button:
    if not api_key:
        st.error("Please set ANTHROPIC_API_KEY in your environment variables!")
    else:
        with st.spinner('Generating your story...'):
            try:
                # Generate the story using Chat
                response = chat(story_prompt)
                story = response.content[0].text
                
                # Create styled first letter
                first_letter = f"<span class='first-letter'>{story[0]}</span>"
                rest_of_story = story[1:]
                
                # Display story in a box with styled first letter
                st.markdown("---")
                st.markdown("### Your Story:")
                story_container = st.container()
                with story_container:
                    st.markdown(f"{first_letter}{rest_of_story}", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")