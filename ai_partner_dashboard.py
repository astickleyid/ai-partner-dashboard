
import streamlit as st
import pandas as pd
import os
import json
import hashlib

# Configurable file paths
CAPABILITIES_FILE = "capabilities.csv"
MEMORY_STACK_FILE = "memory_stack.csv"
AUTH_FILE = "auth.json"

# Required columns
REQUIRED_CAP_COLUMNS = ["Category", "Description", "Level (1-5)"]
REQUIRED_MEM_COLUMNS = ["Section", "Description", "Editable"]

# Hash password for storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load admin credentials
def load_credentials():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            return json.load(f)
    return None

# Save admin credentials
def save_credentials(username, password):
    hashed = hash_password(password)
    with open(AUTH_FILE, "w") as f:
        json.dump({"username": username, "password": hashed}, f)

# Authentication check
def authenticate(username, password):
    creds = load_credentials()
    if creds and creds["username"] == username and creds["password"] == hash_password(password):
        return True
    return False

# Load data safely with defaults
def load_data(filepath, default_data, required_columns):
    try:
        df = pd.read_csv(filepath)
        if all(col in df.columns for col in required_columns):
            return df
        else:
            st.warning(f"File {filepath} is missing required columns. Loading defaults.")
            return pd.DataFrame(default_data)
    except FileNotFoundError:
        # File doesn't exist yet - this is normal on first run
        return pd.DataFrame(default_data)
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}. Loading default data.")
        return pd.DataFrame(default_data)

# Save function
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

# Setup page
st.set_page_config(page_title="AI Partner Dashboard", layout="wide")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Logout functionality
def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""

st.title("AI Partner Dashboard")

# Authentication
auth = load_credentials()

# Check if user is already authenticated
if st.session_state.authenticated:
    # Show user info and logout button in sidebar
    with st.sidebar:
        st.success(f"Logged in as: {st.session_state.username}")
        if st.button("Logout"):
            logout()
            st.rerun()
else:
    # Show login/setup forms
    if not auth:
        st.subheader("Administrator Setup")
        st.info("No administrator account found. Please create one to continue.")
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        
        if st.button("Set Administrator"):
            if not new_user or not new_pass or not confirm_pass:
                st.error("All fields are required.")
            elif len(new_pass) < 6:
                st.error("Password must be at least 6 characters long.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            else:
                save_credentials(new_user, new_pass)
                st.success("Administrator account created successfully!")
                st.info("Please refresh the page and log in with your credentials.")
        st.stop()
    else:
        st.subheader("Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Login"):
                if authenticate(user, pwd):
                    st.session_state.authenticated = True
                    st.session_state.username = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        
        if not user or not pwd:
            st.warning("Please enter your credentials to continue.")
        st.stop()

# Load data
capabilities_df = load_data(CAPABILITIES_FILE, def_capabilities, REQUIRED_CAP_COLUMNS)
memory_stack_df = load_data(MEMORY_STACK_FILE, def_memory_stack, REQUIRED_MEM_COLUMNS)

# Validate capabilities data
def validate_capabilities(df):
    errors = []
    if df.empty:
        return errors
    
    # Check for required columns
    for col in REQUIRED_CAP_COLUMNS:
        if col not in df.columns:
            errors.append(f"Missing required column: {col}")
    
    # Validate Level values
    if "Level (1-5)" in df.columns:
        invalid_levels = df[~df["Level (1-5)"].astype(str).str.match(r'^[1-5]$')]
        if not invalid_levels.empty:
            errors.append("Level must be between 1 and 5")
    
    return errors

# Validate memory stack data
def validate_memory_stack(df):
    errors = []
    if df.empty:
        return errors
    
    # Check for required columns
    for col in REQUIRED_MEM_COLUMNS:
        if col not in df.columns:
            errors.append(f"Missing required column: {col}")
    
    return errors

# Dashboard tabs
def render_capabilities_dashboard():
    st.subheader("Skill Capability Dashboard")
    st.markdown("Track AI capabilities across different categories with proficiency levels (1-5)")
    
    edited_df = st.data_editor(
        capabilities_df, 
        num_rows="dynamic", 
        use_container_width=True, 
        key="cap_editor",
        column_config={
            "Level (1-5)": st.column_config.NumberColumn(
                "Level (1-5)",
                help="Proficiency level from 1 (basic) to 5 (expert)",
                min_value=1,
                max_value=5,
                step=1,
            )
        }
    )
    
    if not edited_df.equals(capabilities_df):
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("💾 Save Capabilities", type="primary"):
                errors = validate_capabilities(edited_df)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    saved = save_data(edited_df, CAPABILITIES_FILE)
                    if saved:
                        st.success("✅ Capabilities saved successfully!")
                        st.rerun()
        with col2:
            st.caption("⚠️ You have unsaved changes")
    else:
        st.caption("✓ All changes saved")

def render_memory_stack_dashboard():
    st.subheader("Memory Stack Dashboard")
    st.markdown("Organize AI memory into structured sections for better context management")
    
    edited_df = st.data_editor(
        memory_stack_df, 
        num_rows="dynamic", 
        use_container_width=True, 
        key="mem_editor"
    )
    
    if not edited_df.equals(memory_stack_df):
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("💾 Save Memory Stack", type="primary"):
                errors = validate_memory_stack(edited_df)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    saved = save_data(edited_df, MEMORY_STACK_FILE)
                    if saved:
                        st.success("✅ Memory Stack saved successfully!")
                        st.rerun()
        with col2:
            st.caption("⚠️ You have unsaved changes")
    else:
        st.caption("✓ All changes saved")

# Sidebar information
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Dashboard Info")
    st.markdown("**Version:** 1.0.0")
    st.markdown("**User:** " + st.session_state.username)
    
    # Show data file status
    cap_exists = os.path.exists(CAPABILITIES_FILE)
    mem_exists = os.path.exists(MEMORY_STACK_FILE)
    
    st.markdown("### 💾 Data Files")
    st.markdown(f"Capabilities: {'✅' if cap_exists else '📝 Using defaults'}")
    st.markdown(f"Memory Stack: {'✅' if mem_exists else '📝 Using defaults'}")
    
    st.markdown("---")
    st.markdown("### 📖 Help")
    st.markdown("""
    - Click cells to edit
    - Use toolbar to add/remove rows
    - Export data as CSV
    - Save button appears when changes are made
    """)

# Display dashboards
tab1, tab2 = st.tabs(["📊 Skill Capability Dashboard", "🧠 Memory Stack Dashboard"])
with tab1:
    render_capabilities_dashboard()
with tab2:
    render_memory_stack_dashboard()
