"""
Dashboard Page: Premium Dark Mode SaaS Edition
High-end visualizations for Neuro Index with glassmorphism design.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from utils.data_manager import DataManager


# Premium color palette (Tailwind-inspired)
EMERALD_500 = '#10B981'  # Primary green
ROSE_500 = '#F43F5E'      # Accent red
BLUE_500 = '#3B82F6'      # Primary blue
VIOLET_500 = '#8B5CF6'    # Accent purple
SLATE_400 = '#94a3b8'     # Text gray
DEEP_SLATE = '#0B1120'    # Background


def normalize_to_percent(value, max_value):
    """Normalize a score to 0-100% for fair comparison."""
    return (value / max_value) * 100


def create_waterfall_chart(latest_entry):
    """
    Chart 1: The Score Waterfall (Truth Teller)
    Shows how each component contributes to the final score.
    """
    # Extract components
    study_score = latest_entry.get('study_score', 0)
    recall_score = latest_entry.get('recall_score', 0)
    sleep_score = latest_entry.get('sleep_score', 0)
    diet_score = latest_entry.get('diet_score', 0)
    exercise_score = latest_entry.get('exercise_score', 0)
    sunlight_score = latest_entry.get('sunlight_score', 0)
    circadian_penalty = latest_entry.get('circadian_penalty', 0)
    distraction_penalty = latest_entry.get('distraction_penalty', 0)
    total = latest_entry.get('total_index', 0)
    
    # Waterfall data
    fig = go.Figure(go.Waterfall(
        name="Score Breakdown",
        orientation="v",
        measure=[
            "absolute",  # Base
            "relative",  # Study
            "relative",  # Recall
            "relative",  # Sleep
            "relative",  # Diet
            "relative",  # Exercise
            "relative",  # Sunlight
            "relative",  # Circadian
            "relative",  # Distraction
            "total"      # Total
        ],
        x=[
            "Base",
            "Study",
            "Recall",
            "Sleep",
            "Diet",
            "Exercise",
            "☀️ Solar",
            "Circadian",
            "Distraction",
            "Total"
        ],
        y=[
            0,
            study_score,
            recall_score,
            sleep_score,
            diet_score,
            exercise_score,
            sunlight_score,
            circadian_penalty,
            distraction_penalty,
            0
        ],
        text=[
            "",
            f"+{study_score}",
            f"+{recall_score}",
            f"+{sleep_score}",
            f"+{diet_score}",
            f"+{exercise_score}",
            f"+{sunlight_score}",
            f"{circadian_penalty}",
            f"{distraction_penalty}",
            f"{total}"
        ],
        textposition="outside",
        textfont=dict(family='JetBrains Mono, monospace', size=11, color=SLATE_400),
        increasing={"marker": {"color": EMERALD_500}},
        decreasing={"marker": {"color": ROSE_500}},
        totals={"marker": {"color": BLUE_500}},
        connector={"line": {"color": 'rgba(255, 255, 255, 0.05)', "width": 2}},
        hovertemplate='<b>%{x}</b><br>Value: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "🎯 Score Waterfall",
            'font': {'size': 18, 'color': SLATE_400, 'family': 'Inter, sans-serif'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=SLATE_400, family='Inter, sans-serif', size=11),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=True,
            color=SLATE_400
        ),
        yaxis=dict(
            title="Points",
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=True,
            range=[-15, 110],
            color=SLATE_400
        ),
        height=400,
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig


def create_radar_chart(latest_entry):
    """
    Chart 2: The Neuro-Radar Hexagon
    Normalized view of all 6 components.
    """
    categories = ['Study', 'Recall', 'Sleep', 'Diet', 'Exercise', '☀️ Solar']
    
    normalized_scores = [
        normalize_to_percent(latest_entry.get('study_score', 0), 30),
        normalize_to_percent(latest_entry.get('recall_score', 0), 20),
        normalize_to_percent(latest_entry.get('sleep_score', 0), 20),
        normalize_to_percent(latest_entry.get('diet_score', 0), 20),
        normalize_to_percent(latest_entry.get('exercise_score', 0), 10),
        normalize_to_percent(latest_entry.get('sunlight_score', 0), 5)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_scores,
        theta=categories,
        fill='toself',
        fillcolor=f'rgba(16, 185, 129, 0.2)',
        line=dict(color=EMERALD_500, width=3),
        marker=dict(
            color=EMERALD_500,
            size=10,
            symbol='circle',
            line=dict(color=BLUE_500, width=2)
        ),
        name='Current Scores',
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.05)',
                tickfont=dict(color=SLATE_400, size=9, family='Inter, sans-serif')
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.05)',
                tickfont=dict(color=SLATE_400, size=12, family='Inter, sans-serif'),
                linecolor='rgba(255, 255, 255, 0.05)'
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        title={
            'text': "🧠 Neuro-Radar",
            'font': {'size': 18, 'color': SLATE_400, 'family': 'Inter, sans-serif'}
        },
        font=dict(color=SLATE_400, family='Inter, sans-serif'),
        height=400,
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig


def show_dashboard():
    """Main dashboard display function."""
    # This is called from app.py when dashboard mode is active
    # The actual dashboard code will be at the bottom of this file
    pass


def create_grind_vs_growth_timeline(df, days=30):
    """
    Chart 3: "Grind vs. Growth" Timeline
    Dual axis: Study vs Screen Time (bars) + Total Index (line)
    
    Args:
        df: DataFrame with data
        days: Number of days to show (14, 30, 60, 90)
    """
    if df.empty or len(df) < 2:
        fig = go.Figure()
        fig.add_annotation(
            text="Not enough data",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color=SLATE_400, family='Inter, sans-serif')
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        return fig
    
    # Sort by date
    df = df.sort_values('date')
    
    # Filter to last N days by actual date (or all available if less)
    max_date = df['date'].max()
    cutoff_date = max_date - pd.Timedelta(days=days-1)
    df = df[df['date'] >= cutoff_date]
    
    df['date_str'] = df['date'].dt.strftime('%b %d')
    df['screen_time_hours'] = df['screen_time_minutes'] / 60
    
    fig = go.Figure()
    
    # Bar: Study Hours (Green)
    fig.add_trace(go.Bar(
        x=df['date_str'],
        y=df['study_hours'],
        name='Study Hours',
        marker=dict(color=EMERALD_500),
        yaxis='y',
        opacity=0.8,
        hovertemplate='<b>Study</b><br>Hours: %{y:.1f}<extra></extra>'
    ))
    
    # Bar: Screen Time (Red)
    fig.add_trace(go.Bar(
        x=df['date_str'],
        y=df['screen_time_hours'],
        name='Screen Time',
        marker=dict(color=ROSE_500),
        yaxis='y',
        opacity=0.8,
        hovertemplate='<b>Screen</b><br>Hours: %{y:.1f}<extra></extra>'
    ))
    
    # Line: Total Index (Cyan - Solid, Prominent)
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['total_index'],
        name='Total Index',
        mode='lines+markers',
        line=dict(color='#00F0FF', width=4, dash='solid'),  # Bright cyan, solid line
        marker=dict(size=10, color='#00F0FF', symbol='diamond', line=dict(color='#ffffff', width=1)),
        yaxis='y2',
        hovertemplate='<b>Total Index</b><br>Score: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "⚡ Grind vs. Growth Timeline",
            'font': {'size': 18, 'color': SLATE_400, 'family': 'Inter, sans-serif'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=SLATE_400, family='Inter, sans-serif'),
        xaxis=dict(
            title="Date",
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=True,
            tickangle=-45,
            color=SLATE_400
        ),
        yaxis=dict(
            title="Hours",
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=True,
            side='left',
            range=[0, max(df['study_hours'].max(), df['screen_time_hours'].max()) * 1.2],
            color=SLATE_400
        ),
        yaxis2=dict(
            title="Total Index",
            overlaying='y',
            side='right',
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=False,
            range=[0, 100],
            color=SLATE_400
        ),
        barmode='group',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10, family='Inter, sans-serif')
        ),
        margin=dict(l=50, r=50, t=70, b=80)
    )
    
    return fig


def create_cognitive_roi_trend(df, days=30):
    """
    Chart 4: Cognitive ROI Trend
    Line chart showing ROI over time, colored by sleep hours
    
    Args:
        df: DataFrame with data
        days: Number of days to show (14, 30, 60, 90)
    """
    if df.empty or len(df) < 2:
        fig = go.Figure()
        fig.add_annotation(
            text="Not enough data",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color=SLATE_400, family='Inter, sans-serif')
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        return fig
    
    df = df.sort_values('date')
    
    # Filter to last N days (or all available if less)
    if len(df) > days:
        df = df.tail(days)
    
    df['date_str'] = df['date'].dt.strftime('%b %d')
    
    # Create figure
    fig = go.Figure()
    
    # Add scatter trace with color mapped to sleep hours (solid line for calculated metric)
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['cognitive_roi'],
        mode='lines+markers',
        marker=dict(
            size=11,
            color=df['sleep_hours'],
            colorscale=[[0, ROSE_500], [0.5, '#FFD700'], [1, EMERALD_500]],
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="Sleep Hours",
                    font=dict(color=SLATE_400, family='Inter, sans-serif')
                ),
                tickfont=dict(color=SLATE_400, family='Inter, sans-serif')
            ),
            line=dict(color='#ffffff', width=1.5)
        ),
        line=dict(color='#BF00FF', width=3.5, dash='solid'),  # Purple solid line for calculated metric
        name='Cognitive ROI',
        hovertemplate='<b>Cognitive ROI</b><br>Value: %{y:.2f}<br>Sleep: %{marker.color:.1f}h<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "🧠 Cognitive ROI Trend",
            'font': {'size': 18, 'color': SLATE_400, 'family': 'Inter, sans-serif'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=SLATE_400, family='Inter, sans-serif'),
        xaxis=dict(
            title="Date",
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=True,
            tickangle=-45,
            color=SLATE_400
        ),
        yaxis=dict(
            title="ROI (Recall % / Study Hour)",
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=True,
            color=SLATE_400
        ),
        height=400,
        showlegend=False,
        margin=dict(l=50, r=50, t=60, b=80)
    )
    
    return fig


def create_comprehensive_timeline(df, days=30):
    """
    Chart 5: Comprehensive Multi-Metric Timeline
    Shows all user inputs and calculated indices over time
    
    Args:
        df: DataFrame with data
        days: Number of days to show (14, 30, 60, 90)
    """
    if df.empty or len(df) < 2:
        fig = go.Figure()
        fig.add_annotation(
            text="Not enough data",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color=SLATE_400, family='Inter, sans-serif')
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500
        )
        return fig
    
    # Sort by date
    df = df.sort_values('date')
    
    # Filter to last N days by actual date (or all available if less)
    max_date = df['date'].max()
    cutoff_date = max_date - pd.Timedelta(days=days-1)
    df = df[df['date'] >= cutoff_date]
    
    df['date_str'] = df['date'].dt.strftime('%b %d')
    
    fig = go.Figure()
    
    # User Input Metrics (BOLD lines, semi-transparent)
    # User Input Metrics (DOTTED LINES)
    # Study Hours
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['study_hours'],
        name='Study Hours',
        mode='lines',
        line=dict(color=EMERALD_500, width=2.5, dash='dot'),
        opacity=0.7,
        hovertemplate='<b>Study Hours</b><br>%{y:.1f}h<extra></extra>'
    ))
    
    # Sleep Hours
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['sleep_hours'],
        name='Sleep Hours',
        mode='lines',
        line=dict(color=BLUE_500, width=2.5, dash='dot'),
        opacity=0.7,
        hovertemplate='<b>Sleep Hours</b><br>%{y:.1f}h<extra></extra>'
    ))
    
    # Screen Time (converted to hours)
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['screen_time_minutes'] / 60,
        name='Screen Time (hrs)',
        mode='lines',
        line=dict(color=ROSE_500, width=2.5, dash='dot'),
        opacity=0.7,
        hovertemplate='<b>Screen Time</b><br>%{y:.1f}h<extra></extra>'
    ))
    
    # Recall Percent (scaled down for visibility)
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['recall_percent'] / 10,  # Scale down from 0-100 to 0-10
        name='Recall % (÷10)',
        mode='lines',
        line=dict(color=VIOLET_500, width=2.5, dash='dot'),
        opacity=0.7,
        hovertemplate='<b>Recall</b><br>%{y:.1f} (×10 = ' + df['recall_percent'].astype(str) + '%)<extra></extra>'
    ))
    
    # Diet Quality
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['diet_quality'],
        name='Diet Quality',
        mode='lines',
        line=dict(color='#FFD700', width=2.5, dash='dot'),
        opacity=0.7,
        hovertemplate='<b>Diet Quality</b><br>%{y}/10<extra></extra>'
    ))
    
    # Exercise Minutes (scaled down)
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['exercise_minutes'] / 10,  # Scale down for visibility
        name='Exercise (÷10 min)',
        mode='lines',
        line=dict(color='#FF6B6B', width=2.5, dash='dot'),
        opacity=0.7,
        hovertemplate='<b>Exercise</b><br>%{y:.1f} (×10 = ' + df['exercise_minutes'].astype(str) + ' min)<extra></extra>'
    ))
    
    # Sunlight Minutes (scaled down)
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['sunlight_minutes'] / 10,  # Scale down for visibility
        name='Sunlight (÷10 min)',
        mode='lines',
        line=dict(color='#FFA500', width=2.5, dash='dot'),
        opacity=0.7,
        hovertemplate='<b>Sunlight</b><br>%{y:.1f} (×10 = ' + df['sunlight_minutes'].astype(str) + ' min)<extra></extra>'
    ))
    
    # Calculated Metrics (SOLID BOLD LINES - very prominent)
    # Total Index (most prominent - cyan solid)
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['total_index'] / 10,  # Scale down from 0-100 to 0-10
        name='Total Index (÷10)',
        mode='lines+markers',
        line=dict(color='#00F0FF', width=6, dash='solid'),
        marker=dict(size=10, color='#00F0FF', symbol='diamond', line=dict(color='#ffffff', width=1.5)),
        hovertemplate='<b>Total Index</b><br>%{y:.1f} (×10 = ' + df['total_index'].astype(str) + ')<extra></extra>'
    ))
    
    # Cognitive ROI (bold - purple solid)
    fig.add_trace(go.Scatter(
        x=df['date_str'],
        y=df['cognitive_roi'],
        name='Cognitive ROI',
        mode='lines+markers',
        line=dict(color='#BF00FF', width=5, dash='solid'),
        marker=dict(size=9, color='#BF00FF', symbol='circle'),
        hovertemplate='<b>Cognitive ROI</b><br>%{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "📊 Comprehensive Metrics Timeline",
            'font': {'size': 18, 'color': SLATE_400, 'family': 'Inter, sans-serif'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=SLATE_400, family='Inter, sans-serif', size=10),
        xaxis=dict(
            title="Date",
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=True,
            tickangle=-45,
            color=SLATE_400
        ),
        yaxis=dict(
            title="Value (see legend for scaling)",
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=True,
            color=SLATE_400
        ),
        height=500,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=9, family='Inter, sans-serif'),
            bgcolor='rgba(11, 17, 32, 0.8)',
            bordercolor=SLATE_400,
            borderwidth=1
        ),
        margin=dict(l=50, r=150, t=60, b=80)
    )
    
    return fig


def show_dashboard():
    """Main dashboard display function - called from app.py."""
    # Premium SaaS dark mode styling with glassmorphism
    st.markdown("""
        <style>
        /* Import premium fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        /* Global background */
        .main {
            background-color: #0B1120;
        }
        
        /* Glass card styling */
        .glass-card {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(10px);
            margin-bottom: 20px;
        }
        
        /* Typography */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 600;
        }
        
        /* Metric cards HUD style */
        .metric-hud {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .metric-hud::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--accent-color);
        }
        
        .metric-label {
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 28px;
            font-weight: 600;
            color: #ffffff;
        }
        
        /* Streamlit overrides */
        .stPlotlyChart {
            background: transparent !important;
        }
        
        /* Divider styling */
        hr {
            border: none;
            height: 1px;
            background: rgba(255, 255, 255, 0.08);
            margin: 2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    today = datetime.now().strftime('%B %d, %Y')
    st.title("📊 Neuro Index Dashboard")
    st.markdown(f"<p style='font-family: Inter, sans-serif; color: #94a3b8; font-size: 14px;'>Real-time performance insights • {today}</p>", unsafe_allow_html=True)
    
    # Load data
    data_manager = DataManager("neuro_logs.csv")
    df = data_manager.load_data()
    
    if df.empty:
        st.warning("⚠️ No data available. Please add entries from the main page first.")
        st.stop()
    
    # Get latest entry
    latest = df.iloc[0]
    
    # Custom HUD-style metrics
    st.markdown("<div style='margin: 30px 0;'>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    metrics_data = [
        ("Total Index", f"{latest.get('total_index', 0)}", "/100", BLUE_500, col1),
        ("Study", f"{latest.get('study_score', 0)}", "/30", EMERALD_500, col2),
        ("Recall", f"{latest.get('recall_score', 0)}", "/20", VIOLET_500, col3),
        ("Sleep", f"{latest.get('sleep_score', 0)}", "/20", BLUE_500, col4),
        ("Diet", f"{latest.get('diet_score', 0)}", "/20", EMERALD_500, col5),
        ("Exercise", f"{latest.get('exercise_score', 0)}", "/10", ROSE_500, col6),
    ]
    
    for label, value, suffix, color, col in metrics_data:
        with col:
            st.markdown(f"""
                <div class="metric-hud" style="--accent-color: {color};">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}<span style="font-size: 16px; color: #94a3b8;">{suffix}</span></div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Row 1: Time Series Intelligence
    col_header, col_selector = st.columns([3, 1])
    with col_header:
        st.subheader("📈 Time Series Intelligence")
    with col_selector:
        days_option = st.selectbox(
            "Duration",
            options=[14, 30, 60, 90],
            index=1,  # Default to 30 days
            key="time_series_duration",
            label_visibility="collapsed"
        )
    
    st.markdown(f"<p style='font-family: Inter, sans-serif; color: #94a3b8; font-size: 12px; margin-top: -10px;'>Showing last {days_option} days (or all available data)</p>", unsafe_allow_html=True)
    
    col_timeline, col_roi = st.columns(2)
    
    with col_timeline:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        grind_growth = create_grind_vs_growth_timeline(df, days=days_option)
        st.plotly_chart(grind_growth, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_roi:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        roi_trend = create_cognitive_roi_trend(df, days=days_option)
        st.plotly_chart(roi_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Comprehensive Metrics Timeline (MOVED BEFORE SCORE COMPOSITION)
    st.divider()
    
    col_header2, col_selector2 = st.columns([3, 1])
    with col_header2:
        st.subheader("📊 All Metrics Timeline")
    with col_selector2:
        days_option2 = st.selectbox(
            "Duration",
            options=[14, 30, 60, 90],
            index=1,  # Default to 30 days
            key="comprehensive_timeline_duration",
            label_visibility="collapsed"
        )
    
    st.markdown(f"<p style='font-family: Inter, sans-serif; color: #94a3b8; font-size: 12px; margin-top: -10px;'>All user inputs + calculated indices • Last {days_option2} days</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    comprehensive = create_comprehensive_timeline(df, days=days_option2)
    st.plotly_chart(comprehensive, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Score Composition
    st.divider()
    st.subheader("📊 Score Composition")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        waterfall = create_waterfall_chart(latest)
        st.plotly_chart(waterfall, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        radar = create_radar_chart(latest)
        st.plotly_chart(radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data table
    st.divider()
    st.subheader("📋 Recent Entries")
    
    display_df = df.head(10).copy()
    display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        display_df[[
            'date',
            'total_index',
            'cognitive_roi',
            'study_hours',
            'recall_percent',
            'sleep_hours',
            'sunlight_score',
            'cycle_day'
        ]],
        use_container_width=True,
        hide_index=True
    )

