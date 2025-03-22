
import streamlit as st
import pandas as pd
import os

# Configurable file paths
CAPABILITIES_FILE = "capabilities.csv"
MEMORY_STACK_FILE = "memory_stack.csv"

# Required columns
REQUIRED_CAP_COLUMNS = ["Category", "Description", "Level (1-5)"]
REQUIRED_MEM_COLUMNS = ["Section", "Description", "Editable"]

# Page config
st.set_page_config(page_title="AI Partner Dashboard", layout="wide")

st.title("AI Partner Dashboard")
st.markdown("Access and edit your capabilities and memory stack from anywhere.")

# Data loader with validation and error handling
def load_data(filepath, default_data, required_columns):
    try:
        df = pd.read_csv(filepath)
        if all(col in df.columns for col in required_columns):
            return df
        else:
            st.warning(f"File {filepath} is missing required columns. Loading defaults.")
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}")
    return pd.DataFrame(default_data)

# Save function with error handling
def save_data(dataframe, filepath):
    try:
        dataframe.to_csv(filepath, index=False)
        return True
    except Exception as e:
        st.error(f"Failed to save {filepath}: {e}")
        return False

# Default data
def_capabilities = {
    "Category": ["Research & Analysis", "Creative Thinking", "Execution Support", 
                 "Memory & Alignment", "Self-Auditing"],
    "Description": [
        "Synthesizing complex info, strategy analysis, fact-checking",
        "Ideation, frameworks, lateral thinking",
        "Docs, coding, automation, reports",
        "Long-term memory of user goals and preferences",
        "Output accuracy checks, feedback-driven improvement"
    ],
    "Level (1-5)": [4, 4, 3, 5, 3]
}

def_memory_stack = {
    "Section": [
        "Identity Core", "Vision & Long-Term Objectives", "Values Stack",
        "Strategic Preferences", "Feedback Loop", "Memory Containers"
    ],
    "Description": [
        "Your role, tone, and expectations of me",
        "Your long-term vision, mission, and goals",
        "Core values guiding your decision-making",
        "How you prefer to work and think",
        "How we iterate and improve over time",
        "Categories of memory I will store and update"
    ],
    "Editable": ["Yes", "Yes", "Yes", "Yes", "Yes", "Yes"]
}

# Load data with validation
capabilities_df = load_data(CAPABILITIES_FILE, def_capabilities, REQUIRED_CAP_COLUMNS)
memory_stack_df = load_data(MEMORY_STACK_FILE, def_memory_stack, REQUIRED_MEM_COLUMNS)

# UI rendering functions
def render_capabilities_dashboard():
    st.subheader("Skill Capability Dashboard")
    edited_df = st.data_editor(capabilities_df, num_rows="dynamic", use_container_width=True, key="cap_editor")
    if not edited_df.equals(capabilities_df):
        if st.button("Save Capabilities"):
            saved = save_data(edited_df, CAPABILITIES_FILE)
            if saved:
                st.success("Capabilities saved successfully.")
    else:
        st.info("No changes detected in capabilities.")

def render_memory_stack_dashboard():
    st.subheader("Memory Stack Dashboard")
    edited_df = st.data_editor(memory_stack_df, num_rows="dynamic", use_container_width=True, key="mem_editor")
    if not edited_df.equals(memory_stack_df):
        if st.button("Save Memory Stack"):
            saved = save_data(edited_df, MEMORY_STACK_FILE)
            if saved:
                st.success("Memory Stack saved successfully.")
    else:
        st.info("No changes detected in memory stack.")

# Render tabs
tab1, tab2 = st.tabs(["Skill Capability Dashboard", "Memory Stack Dashboard"])

with tab1:
    render_capabilities_dashboard()

with tab2:
    render_memory_stack_dashboard()
