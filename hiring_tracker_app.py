import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(page_title="Hiring Tracker", layout="wide")
st.title("Parking Department Applicant Tracker")

# --- Constants & Setup ---
STAGES = [
    "Applied", "Initial Screening", "Interview Scheduled", 
    "Offer Extended", "Background/MVR Check", "Onboarding/Tech Setup", "First Day"
]
ROLES = ["Attendent", "Event"]

# Initialize session state to act as our database
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Name": ["Alex Rivers", "Jordan Lee", "Casey Smith", "Morgan Case"],
        "Role": ["Attendent", "Event", "Attendent", "Event"],
        "Stage": ["Interview Scheduled", "Applied", "Background/MVR Check", "Onboarding/Tech Setup"],
        "Target Start Date": ["2026-06-15", "2026-06-20", "2026-06-10", "2026-06-01"]
    })

# --- Sidebar: Add New Candidate ---
with st.sidebar:
    st.header("Add New Candidate")
    with st.form("add_candidate_form", clear_on_submit=True):
        new_name = st.text_input("Candidate Name")
        new_role = st.selectbox("Role", ROLES)
        new_stage = st.selectbox("Current Stage", STAGES)
        new_date = st.date_input("Target Start Date")
        
        submitted = st.form_submit_button("Add to Pipeline")
        if submitted and new_name:
            new_data = pd.DataFrame([{
                "Name": new_name, "Role": new_role, 
                "Stage": new_stage, "Target Start Date": str(new_date)
            }])
            st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
            st.success(f"Added {new_name}!")

# --- Main Dashboard Tabs ---
tab1, tab2, tab3 = st.tabs(["📋 Pipeline (Kanban)", "📊 Analytics", "🗄️ Raw Data Edit"])

# TAB 1: Pipeline
with tab1:
    st.subheader("Current Candidate Pipeline")
    
    cols = st.columns(len(STAGES))
    for i, stage in enumerate(STAGES):
        with cols[i]:
            st.markdown(f"**{stage}**")
            stage_df = st.session_state.df[st.session_state.df["Stage"] == stage]
            
            for index, row in stage_df.iterrows():
                with st.container():
                    st.info(f"**{row['Name']}**\n\n*{row['Role']}*")
                    
                    if i < len(STAGES) - 1:
                        next_stage = STAGES[i+1]
                        if st.button(f"Move ➔", key=f"move_{index}"):
                            st.session_state.df.at[index, "Stage"] = next_stage
                            st.rerun()

# TAB 2: Analytics & Graphics
with tab2:
    st.subheader("Hiring Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        stage_counts = st.session_state.df["Stage"].value_counts().reset_index()
        stage_counts.columns = ["Stage", "Count"]
        fig1 = px.bar(stage_counts, x="Stage", y="Count", title="Candidates by Stage")
        st.plotly_chart(fig1, width="stretch")
        
    with col2:
        role_counts = st.session_state.df["Role"].value_counts().reset_index()
        role_counts.columns = ["Role", "Count"]
        fig2 = px.pie(role_counts, names="Role", values="Count", title="Distribution of Roles")
        st.plotly_chart(fig2, width="stretch")

# TAB 3: Raw Data & Editing
with tab3:
    st.subheader("Database Overview")
    st.write("Edit candidate details directly below. Changes save automatically.")
    
    edited_df = st.data_editor(
        st.session_state.df, 
        use_container_width=True, 
        num_rows="dynamic"
    )
    st.session_state.df = edited_df
