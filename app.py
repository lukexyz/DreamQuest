import streamlit as st
from claudette import *
import os
from utils import load_css

# Set page config
st.set_page_config(
    page_title="Dreamweaver",
    page_icon="📚",
    layout="centered"
)

# Load custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Initialize session state for managing expander state
if 'expander_state' not in st.session_state:
    st.session_state.expander_state = True

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
st.title("📚 Story Time")

# Create collapsible section for inputs
with st.expander("Story Customization Options", expanded=st.session_state.expander_state):
    # Create two columns
    left_col, right_col = st.columns(2)

    with left_col:
        # Basic Input fields
        age = st.number_input("Child's Age", min_value=2, max_value=12, value=6)
        story_length = st.selectbox(
            "Story Length",
            options=["Short (100 words)", "Medium (300 words)", "Long (500 words)"]
        )
        
        # Story Setting
        setting_suggestions = [
            "Choose a setting...",
            "Magical Forest", 
            "Space Station", 
            "Underwater Kingdom", 
            "Cozy Home",
            "School Playground",
            "Ancient Castle",
            "Other"
        ]
        setting = st.selectbox("Story Setting", setting_suggestions)
        if setting == "Other":
            setting = st.text_input("Enter custom setting")
        
        # Plot/What Happens
        plot_suggestions = [
            "Choose what happens...",
            "Making a New Friend",
            "Solving a Mystery",
            "Learning a New Skill",
            "Overcoming a Fear",
            "Going on an Adventure",
            "Other"
        ]
        plot = st.selectbox("What Happens", plot_suggestions)
        if plot == "Other":
            plot = st.text_input("Enter custom plot")
        
        # Character Names
        st.subheader("Characters")
        num_characters = st.number_input("Number of Characters", min_value=1, max_value=5, value=2)
        characters = []
        for i in range(num_characters):
            char_name = st.text_input(f"Character {i+1} Name", value=f"Character {i+1}")
            char_trait = st.text_input(f"Character {i+1} Trait", placeholder="e.g., brave, curious, helpful")
            characters.append({"name": char_name, "trait": char_trait})
        
        # Today's Context
        st.subheader("Today's Context")
        todays_activity = st.text_area(
            "What activities or lessons happened today?",
            placeholder="e.g., learned about sharing at school, visited the zoo, practiced counting"
        )
        moral_lesson = st.text_input(
            "What lesson would you like to reinforce?",
            placeholder="e.g., importance of friendship, being brave, helping others"
        )
        
    with right_col:
        generate_button = st.button("Generate Story")
        
        # Get word count from selection
        word_count = int(story_length.split()[1].strip("()"))

        # Create enhanced story prompt
        story_prompt = f"""Create an engaging story suitable for a {age}-year-old child. 

        Setting: {setting if setting != "Choose a setting..." else "any appropriate setting"}
        Plot: {plot if plot != "Choose what happens..." else "any engaging plot"}

        Characters:
        {chr(10).join([f"- {char['name']}: {char['trait']}" if char['trait'] else f"- {char['name']}" for char in characters])}

        Context from today:
        Activities: {todays_activity if todays_activity else "Not specified"}
        Lesson to reinforce: {moral_lesson if moral_lesson else "Include an age-appropriate moral lesson"}

        The story should be approximately {word_count} words long, be both entertaining and educational, 
        and naturally incorporate these elements without feeling forced.
        Only return the story itself, no title or additional commentary."""

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
                
                # Close the expander after generating the story
                st.session_state.expander_state = False
                
                # Display story in a box with styled first letter
                st.markdown("---")
                st.markdown("### Your Story:")
                story_container = st.container()
                with story_container:
                    st.markdown(f"{first_letter}{rest_of_story}", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.expander_state = True  # Keep expander open if there's an error

# Reset button
if st.button("Start New Story"):
    st.session_state.expander_state = True
    st.rerun()