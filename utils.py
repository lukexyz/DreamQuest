
# Custom CSS styles for the Streamlit app
def load_css():
    return """
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
    """