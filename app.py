"""
UPSC Neuro-OS - Main Entry Point
=================================
A Production-Ready Modular Streamlit Application for UPSC Preparation & Cognitive Performance Tracking

Architecture:
- app.py: Main entry point and application controller
- config/: Configuration settings and constants
- modules/: Core business logic and data processing (scoring_engine, data_manager)
- ui/: Streamlit UI components and renderers (style_loader, charts, background)
- assets/: Static files (CSS, images)
- data/: Local data storage (CSV files)

Author: Senior Python Software Architect
Date: November 29, 2025
"""

import streamlit as st
from datetime import datetime, date
import pandas as pd

# Import configuration
from config.settings import (
    PAGE_CONFIG, APP_TITLE, APP_ICON,
    MAX_SCORES, MIN_SCORES,
    NEON_GREEN, CYBER_CYAN, ELECTRIC_PURPLE
)

# Import modules
from modules.scoring_engine import NeuroScorer
from modules.data_manager import DataManager

# Import UI components
from ui.style_loader import load_css, create_header, styled_metric, inject_custom_html
from ui.charts import render_dashboard_charts
from ui.background import render_neural_background


# Configure the Streamlit page (must be the first Streamlit command)
st.set_page_config(**PAGE_CONFIG)


def initialize_session_state():
    """Initialize session state variables for data persistence."""
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
    
    if 'data' not in st.session_state:
        st.session_state.data = st.session_state.data_manager.load_data()
    
    if 'scorer' not in st.session_state:
        st.session_state.scorer = NeuroScorer()
    
    if 'last_save' not in st.session_state:
        st.session_state.last_save = None
    
    if 'show_mock_data' not in st.session_state:
        st.session_state.show_mock_data = False
    
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = "Daily Log Entry"


def render_data_entry_form():
    """
    Render the data entry form in the main area (not sidebar).
    
    Returns:
        bool: True if data was saved successfully
    """
    st.markdown(
        '<h2 class="neon-text-green">📝 Daily Log Entry</h2>',
        unsafe_allow_html=True
    )
    
    # Date selection
    entry_date = st.date_input(
        "Date",
        value=date.today(),
        max_value=date.today(),
        help="Select the date for this log entry"
    )
    
    st.divider()
    
    # Sleep Section
    st.markdown("### 🌙 Sleep Data")
    col1, col2 = st.columns(2)
    with col1:
        bedtime = st.time_input(
            "Bedtime",
            value=datetime.strptime("22:30", "%H:%M").time(),
            help="What time did you go to bed?"
        )
    with col2:
        wake_time = st.time_input(
            "Wake Time",
            value=datetime.strptime("06:00", "%H:%M").time(),
            help="What time did you wake up?"
        )
    
    sleep_hours = st.number_input(
        "Sleep (hours)",
        min_value=0.0,
        max_value=16.0,
        value=7.5,
        step=0.5,
        help="Total hours of sleep"
    )
    
    st.divider()
    
    # Activity Section
    st.markdown("### 💪 Activity Data")
    col5, col6 = st.columns(2)
    with col5:
        study_hours = st.number_input(
            "Study (hours)",
            min_value=0.0,
            max_value=16.0,
            value=8.0,
            step=0.5,
            help="Total study hours"
        )
    with col6:
        exercise_minutes = st.slider(
            "Exercise (min)",
            min_value=0,
            max_value=120,
            value=45,
            help="Minutes of physical exercise"
        )
    
    st.divider()
    
    # Cognitive Section
    st.markdown("### 🧠 Cognitive Metrics")
    col7, col8 = st.columns(2)
    with col7:
        diet_quality = st.slider(
            "Diet Quality",
            min_value=0,
            max_value=10,
            value=7,
            help="Rate your diet quality (0-10)"
        )
    with col8:
        recall_percent = st.slider(
            "Recall %",
            min_value=0,
            max_value=100,
            value=80,
            help="Percentage of material recalled"
        )
    
    pvt_avg_ms = st.number_input(
        "PVT Reaction Time (ms)",
        min_value=100,
        max_value=1000,
        value=280,
        step=10,
        help="Average reaction time from PVT game"
    )
    
    st.divider()
    
    # Lifestyle Section
    st.markdown("### 🌞 Lifestyle")
    col9, col10, col11 = st.columns(3)
    with col9:
        water_intake_liters = st.number_input(
            "Water (L)",
            min_value=0.0,
            max_value=8.0,
            value=2.5,
            step=0.5,
            help="Water intake in liters"
        )
    with col10:
        screen_time_minutes = st.number_input(
            "Screen Time (min)",
            min_value=0,
            max_value=960,
            value=270,
            step=15,
            help="Non-study screen time in minutes"
        )
    with col11:
        sunlight_minutes = st.number_input(
            "Sunlight (min)",
            min_value=0,
            max_value=720,
            value=60,
            step=15,
            help="Minutes of sunlight exposure"
        )
    
    st.divider()
    
    # Save button
    save_clicked = st.button(
        "💾 Save Entry",
        type="primary",
        use_container_width=True
    )
    
    if save_clicked:
        # Calculate scores using NeuroScorer
        scorer = st.session_state.scorer
        
        # Calculate individual scores
        sleep_score = scorer.calculate_sleep_score(sleep_hours)
        pvt_score = scorer.calculate_pvt_score(pvt_avg_ms)
        circadian_penalty = scorer.calculate_circadian_penalty(
            bedtime.strftime("%H:%M"),
            wake_time.strftime("%H:%M")
        )
        
        # Calculate total index
        metrics = {
            'sleep_score': sleep_score,
            'pvt_score': pvt_score,
            'diet_quality': diet_quality,
            'recall_percent': recall_percent,
            'exercise_minutes': exercise_minutes,
            'circadian_penalty': circadian_penalty
        }
        total_index = scorer.calculate_total_index(metrics)
        
        # Create entry dictionary
        entry = {
            'date': entry_date.strftime("%Y-%m-%d"),
            'sleep_hours': sleep_hours,
            'bedtime': bedtime.strftime("%H:%M"),
            'wake_time': wake_time.strftime("%H:%M"),
            'study_hours': study_hours,
            'exercise_minutes': exercise_minutes,
            'diet_quality': diet_quality,
            'recall_percent': recall_percent,
            'pvt_avg_ms': pvt_avg_ms,
            'water_intake_liters': water_intake_liters,
            'screen_time_minutes': screen_time_minutes,
            'sunlight_minutes': sunlight_minutes,
            'total_index': total_index
        }
        
        # Save entry
        success = st.session_state.data_manager.save_entry(entry)
        
        if success:
            st.success("✅ Entry saved successfully!")
            st.session_state.last_save = datetime.now()
            # Reload data
            st.session_state.data = st.session_state.data_manager.load_data()
            st.balloons()
        else:
            st.error("❌ Failed to save entry")
    
    # Show recent entries table if data exists
    df = st.session_state.data
    if not df.empty:
        st.divider()
        st.markdown("### 📋 Recent Entries")
        
        # Show last 5 entries
        display_df = df.head(5)[['date', 'sleep_hours', 'study_hours', 'total_index']].copy()
        display_df.columns = ['Date', 'Sleep (hrs)', 'Study (hrs)', 'Score']
        st.dataframe(display_df, use_container_width=True, hide_index=True)


def render_main_dashboard():
    """Render the main dashboard with charts and metrics."""
    
    # Load data
    df = st.session_state.data
    
    # Show mock data option if no data exists
    if df.empty:
        st.info("📊 No data available. Toggle to Daily Log Entry to add data, or load mock data for testing.")
        
        col_mock1, col_mock2, col_mock3 = st.columns([1, 1, 1])
        with col_mock2:
            if st.button("🎲 Load Mock Data (7 days)", use_container_width=True):
                mock_df = st.session_state.data_manager.get_mock_data(7)
                for _, row in mock_df.iterrows():
                    st.session_state.data_manager.save_entry(row.to_dict())
                st.session_state.data = st.session_state.data_manager.load_data()
                st.rerun()
        
        st.stop()
    
    # Calculate latest metrics
    latest_entry = df.iloc[0] if not df.empty else None
    
    if latest_entry is not None:
        # Display key metrics
        st.markdown("### 📊 Latest Performance Metrics")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            metric_html = styled_metric(
                "Total Index",
                f"{latest_entry['total_index']}/100",
                None
            )
            inject_custom_html(metric_html)
        
        with col2:
            category, desc = st.session_state.scorer.get_performance_category(
                latest_entry['total_index']
            )
            metric_html = styled_metric(
                "Category",
                category,
                None
            )
            inject_custom_html(metric_html)
        
        with col3:
            metric_html = styled_metric(
                "Sleep",
                f"{latest_entry['sleep_hours']:.1f}h",
                f"Bedtime: {latest_entry['bedtime']}"
            )
            inject_custom_html(metric_html)
        
        with col4:
            metric_html = styled_metric(
                "Diet Quality",
                f"{latest_entry['diet_quality']}/10",
                f"Exercise: {latest_entry['exercise_minutes']}m"
            )
            inject_custom_html(metric_html)
        
        with col5:
            metric_html = styled_metric(
                "PVT / Recall",
                f"{latest_entry['pvt_avg_ms']}ms",
                f"Recall: {latest_entry['recall_percent']}%"
            )
            inject_custom_html(metric_html)
    
    st.divider()
    
    # Render charts in tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Dashboard Overview",
        "🌙 Bio-Rhythm Analysis",
        "🎯 Focus & Productivity",
        "🧠 Cognitive Performance"
    ])
    
    # Generate charts
    bio_fig, focus_fig, cog_fig = render_dashboard_charts(df)
    
    with tab1:
        st.markdown("### 🎨 Comprehensive Performance Dashboard")
        
        # Show all three charts
        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(bio_fig, key="dashboard_bio")
        with col_b:
            st.plotly_chart(focus_fig, key="dashboard_focus")
        
        st.plotly_chart(cog_fig, key="dashboard_cog")
    
    with tab2:
        st.markdown("### 🌙 Bio-Rhythm Analysis")
        st.plotly_chart(bio_fig, key="tab_bio")
        
        # Show stats
        if 'sleep_hours' in df.columns:
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Avg Sleep", f"{df['sleep_hours'].mean():.1f}h")
            with col_s2:
                st.metric("Avg Quality", f"{df['sleep_quality'].mean():.1f}/10")
            with col_s3:
                st.metric("Avg Energy", f"{df['energy_level'].mean():.1f}/10")
    
    with tab3:
        st.markdown("### 🎯 Focus & Productivity Analysis")
        st.plotly_chart(focus_fig, key="tab_focus")
        
        # Show stats
        if 'study_hours' in df.columns:
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                st.metric("Avg Study", f"{df['study_hours'].mean():.1f}h")
            with col_f2:
                st.metric("Avg Focus", f"{df['focus_score'].mean():.1f}/10")
            with col_f3:
                st.metric("Avg Screen Time", f"{df['screen_time_hours'].mean():.1f}h")
    
    with tab4:
        st.markdown("### 🧠 Cognitive Performance Analysis")
        st.plotly_chart(cog_fig, key="tab_cog")
        
        # Show stats
        if 'total_index' in df.columns:
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                st.metric("Avg Index", f"{df['total_index'].mean():.0f}/100")
            with col_c2:
                st.metric("Best Score", f"{df['total_index'].max()}")
            with col_c3:
                st.metric("Avg Recall", f"{df['recall_percent'].mean():.0f}%")
    
    # Footer stats
    st.divider()
    stats = st.session_state.data_manager.get_statistics()
    
    st.markdown(f"""
    <div style="text-align: center; opacity: 0.7; font-size: 0.9rem;">
        <span class="neon-text-cyan">Total Entries:</span> {stats['total_entries']} | 
        <span class="neon-text-cyan">Date Range:</span> {stats['date_range']} | 
        <span class="neon-text-cyan">Best Day:</span> {stats['best_day']} ({stats['best_score']} pts)
    </div>
    """, unsafe_allow_html=True)


def main():
    """
    Main application entry point.
    Orchestrates the entire application flow.
    """
    
    # Load CSS and background
    load_css()
    render_neural_background()
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    header_html = create_header(
        "UPSC Neuro-OS",
        "Cognitive Performance Tracking for UPSC Aspirants"
    )
    inject_custom_html(header_html)
    
    # Add custom CSS for larger toggle
    st.markdown("""
        <style>
        /* Make toggle switch larger and more prominent */
        div[data-testid="stToggle"] {
            transform: scale(1.5);
            transform-origin: center;
            padding: 20px 0;
        }
        div[data-testid="stToggle"] label {
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            color: #00ff41 !important;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Toggle at the top center - larger and more dominant
    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        view_mode_toggle = st.toggle(
            "📊 Performance Metrics",
            value=st.session_state.view_mode == "Performance Metrics",
            help="Toggle ON for Performance Metrics, OFF for Daily Log Entry"
        )
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Update view mode in session state
    view_mode = "Performance Metrics" if view_mode_toggle else "Daily Log Entry"
    st.session_state.view_mode = view_mode
    
    st.divider()
    
    # Render appropriate view
    if view_mode == "Daily Log Entry":
        render_data_entry_form()
    else:
        render_main_dashboard()


if __name__ == "__main__":
    main()
