"""
Neuro Index: Productivity Edition
A Streamlit app for tracking and visualizing study productivity.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, time, date
from utils.scoring import calculate_total_index
from utils.db_data_manager import DataManager, UserConfigManager
from utils.database import init_database


# Page configuration
st.set_page_config(
    page_title="Neuro Index",
    page_icon="🧠",
    layout="wide"
)

# Auto-initialize database tables on startup (safe to call multiple times)
@st.cache_resource
def setup_database():
    """Initialize database tables once on app startup."""
    try:
        init_database()
        return True
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return False

# Initialize database
db_ready = setup_database()


def main():
    """Main application entry point."""
    
    if not db_ready:
        st.error("⚠️ Database not connected. Please check DATABASE_URL environment variable.")
        st.stop()
    
    # Initialize data manager
    data_manager = DataManager()
    config_manager = UserConfigManager()
    
    # Initialize session state for view toggle
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'entry'
    
    # Custom CSS to hide sidebar completely
    st.markdown("""
        <style>
        /* Hide sidebar completely */
        [data-testid="stSidebar"] {
            display: none;
        }
        section[data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.title("🧠 Neuro Index")
    
    # Toggle between Entry and Dashboard with styled buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # Create two buttons for toggle
        col_entry, col_dash = st.columns(2)
        with col_entry:
            if st.button("📝 Entry", key="entry_btn", use_container_width=True, 
                        type="primary" if st.session_state.view_mode == 'entry' else "secondary"):
                st.session_state.view_mode = 'entry'
                st.rerun()
        with col_dash:
            if st.button("📊 Dashboard", key="dash_btn", use_container_width=True,
                        type="primary" if st.session_state.view_mode == 'dashboard' else "secondary"):
                st.session_state.view_mode = 'dashboard'
                st.rerun()
    
    st.divider()
    
    # Show different content based on toggle
    if st.session_state.view_mode == 'dashboard':
        # Import and run dashboard
        from pages.Dashboard import show_dashboard
        show_dashboard()
        return
    
    # Entry mode - centered form (no sidebar)
    st.markdown("### Productivity-First Tracking System")
    
    # Center the form content
    col_left, col_center, col_right = st.columns([1, 3, 1])
    
    with col_center:
        st.header("📊 Daily Log Entry")
        
        # User Settings Section
        with st.expander("⚙️ User Settings", expanded=False):
            st.markdown("**Cycle Tracking Configuration**")
            
            current_period_date = config_manager.get_last_period_date()
            period_date_input = st.date_input(
                "Last Period Start Date",
                value=current_period_date if current_period_date else date.today(),
                help="Date of your last period start - used to auto-calculate cycle day"
            )
            
            if st.button("💾 Save Settings", use_container_width=True):
                config_manager.set_last_period_date(period_date_input)
                st.success("✅ Settings saved!")
                st.rerun()
        
        # Calculate current cycle day
        cycle_day = config_manager.calculate_cycle_day()
        cycle_phase = config_manager.get_cycle_phase(cycle_day)
        
        # Display cycle info
        st.info(f"🌙 **Cycle Day:** {cycle_day} - {cycle_phase}")
        
        # Date selector OUTSIDE the form for reactivity
        entry_date = st.date_input(
            "📅 Entry Date",
            value=date.today(),
            max_value=date.today(),
            help="Select today or a past date to add/edit entry"
        )
        
        # Load existing data for selected date
        existing_data = data_manager.load_data()
        existing_entry = None
        if not existing_data.empty:
            date_str = entry_date.strftime('%Y-%m-%d')
            if 'date' in existing_data.columns:
                existing_data['date'] = pd.to_datetime(existing_data['date']).dt.strftime('%Y-%m-%d')
                match = existing_data[existing_data['date'] == date_str]
                if not match.empty:
                    existing_entry = match.iloc[0].to_dict()
                    st.success(f"📝 Editing existing entry for {entry_date.strftime('%b %d, %Y')}")
        
        # Set default values (from existing entry or defaults)
        def get_val(key, default, dtype=float):
            if existing_entry and key in existing_entry:
                val = existing_entry[key]
                if pd.notna(val):
                    return dtype(val)
            return default
        
        with st.form("daily_entry"):
            st.subheader("Study Data")
            study_hours = st.number_input(
                "Study Hours",
                min_value=0.0,
                max_value=24.0,
                value=get_val('study_hours', 6.0),
                step=0.5,
                help="Total hours spent studying"
            )
            
            screen_time_minutes = st.number_input(
                "Screen Time (minutes)",
                min_value=0,
                max_value=1440,
                value=get_val('screen_time_minutes', 60, int),
                step=15,
                help="Leisure screen time (social media, entertainment)"
            )
            
            recall_percent = st.slider(
                "Recall Accuracy (%)",
                min_value=0,
                max_value=100,
                value=get_val('recall_percent', 80, int),
                help="Percentage of material you can accurately recall"
            )
            
            st.subheader("Physical Data")
            
            sleep_hours = st.number_input(
                "Sleep Hours",
                min_value=0.0,
                max_value=24.0,
                value=get_val('sleep_hours', 7.5),
                step=0.5,
                help="Total hours of sleep"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                # Parse existing bedtime if available
                default_bedtime = time(22, 30)
                if existing_entry and 'bedtime' in existing_entry and pd.notna(existing_entry['bedtime']):
                    try:
                        bt = existing_entry['bedtime']
                        if isinstance(bt, str):
                            default_bedtime = datetime.strptime(bt, '%H:%M:%S').time()
                    except:
                        pass
                bedtime = st.time_input(
                    "Bedtime",
                    value=default_bedtime,
                    help="Time you went to bed"
                )
            
            with col2:
                # Parse existing wake_time if available
                default_wake = time(6, 0)
                if existing_entry and 'wake_time' in existing_entry and pd.notna(existing_entry['wake_time']):
                    try:
                        wt = existing_entry['wake_time']
                        if isinstance(wt, str):
                            default_wake = datetime.strptime(wt, '%H:%M:%S').time()
                    except:
                        pass
                wake_time = st.time_input(
                    "Wake Time",
                    value=default_wake,
                    help="Time you woke up"
                )
            
            diet_quality = st.slider(
                "Diet Quality",
                min_value=0,
                max_value=10,
                value=get_val('diet_quality', 7, int),
                help="Overall diet quality (0=poor, 10=excellent)"
            )
            
            col3, col4 = st.columns(2)
            with col3:
                exercise_minutes = st.number_input(
                    "Exercise (minutes)",
                    min_value=0,
                    max_value=300,
                    value=get_val('exercise_minutes', 45, int),
                    step=5,
                    help="Total minutes of physical exercise"
                )
            
            with col4:
                sunlight_minutes = st.number_input(
                    "Sunlight Exposure (minutes)",
                    min_value=0,
                    max_value=720,
                    value=get_val('sunlight_minutes', 30, int),
                    step=5,
                    help="Minutes of outdoor sunlight exposure"
                )
            
            # Submit button
            submitted = st.form_submit_button("💾 Save Entry", use_container_width=True)
            
            if submitted:
                # Calculate scores
                scores = calculate_total_index(
                    study_hours=study_hours,
                    recall_percent=recall_percent,
                    sleep_hours=sleep_hours,
                    diet_quality=diet_quality,
                    exercise_minutes=exercise_minutes,
                    bedtime=bedtime,
                    wake_time=wake_time,
                    screen_time_minutes=screen_time_minutes,
                    sunlight_minutes=sunlight_minutes
                )
                
                # Calculate cognitive ROI
                from utils.scoring import calculate_cognitive_roi
                cognitive_roi = calculate_cognitive_roi(recall_percent, study_hours)
                
                # Prepare entry
                entry = {
                    'date': datetime.combine(entry_date, datetime.min.time()),
                    'study_hours': study_hours,
                    'screen_time_minutes': screen_time_minutes,
                    'recall_percent': recall_percent,
                    'sleep_hours': sleep_hours,
                    'bedtime': bedtime,
                    'wake_time': wake_time,
                    'diet_quality': diet_quality,
                    'exercise_minutes': exercise_minutes,
                    'sunlight_minutes': sunlight_minutes,
                    'cycle_day': cycle_day,
                    'cognitive_roi': round(cognitive_roi, 2),
                    **scores
                }
                
                # Save entry
                data_manager.save_entry(entry)
                st.success(f"✅ Entry saved! Total Index: {scores['total_index']}/100")
                st.rerun()
    
    # Recent entries section
    st.divider()
    st.subheader("📋 Recent Entries")
    
    df = data_manager.load_data()
    
    if df.empty:
        st.info("👆 Start by entering your daily metrics above!")
        st.markdown("""
        ### Welcome to Neuro Index!
        
        This app helps you track and optimize your productivity through:
        - **Study metrics**: Track study hours and recall accuracy
        - **Physical metrics**: Monitor sleep, diet, and exercise
        - **Smart scoring**: Get a 0-100 productivity index
        - **Penalty system**: Identify distractions and circadian disruptions
        
        Navigate to the **Dashboard** page to see visualizations once you have some data.
        """)
    else:
        # Display latest stats
        latest = df.iloc[0]
        
        st.header("📈 Latest Entry")
        st.markdown(f"**Date:** {latest['date'].strftime('%Y-%m-%d')}")
        
        # Score display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Index",
                f"{latest['total_index']}/100",
                help="Overall productivity score"
            )
        
        with col2:
            st.metric(
                "Study Score",
                f"{latest['study_score']}/30",
                help="Points from study hours"
            )
        
        with col3:
            st.metric(
                "Recall Score",
                f"{latest['recall_score']}/20",
                help="Points from recall accuracy"
            )
        
        # Component breakdown
        st.subheader("Component Breakdown")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Sleep Score", f"{latest['sleep_score']}/20")
        
        with col2:
            st.metric("Diet Score", f"{latest['diet_score']}/20")
        
        with col3:
            st.metric("Exercise Score", f"{latest['exercise_score']}/10")
        
        with col4:
            total_penalties = latest['circadian_penalty'] + latest['distraction_penalty']
            st.metric("Penalties", f"{total_penalties}", delta=f"{total_penalties}")
        
        # Recent history
        st.subheader("Recent History")
        
        display_df = df.head(10).copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        
        # Select columns to display
        display_cols = [
            'date',
            'total_index',
            'study_hours',
            'recall_percent',
            'sleep_hours',
            'circadian_penalty',
            'distraction_penalty'
        ]
        
        st.dataframe(
            display_df[display_cols],
            use_container_width=True,
            hide_index=True
        )


if __name__ == "__main__":
    main()
