"""
UPSC Neuro-OS Chart Components
===============================
Reusable Plotly chart components with neon/cyberpunk theming.
Separates visualization logic from main application.

Author: Senior Python Software Architect
Date: November 29, 2025
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple
import numpy as np

# Import color constants
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import NEON_GREEN, CYBER_CYAN, ELECTRIC_PURPLE, ACCENT_PINK, DEEP_BLUE


# Neon color palette for charts
CHART_COLORS = {
    'green': '#39FF14',
    'cyan': '#00F0FF',
    'purple': '#BF00FF',
    'pink': '#FF006E',
    'orange': '#FF8C00',
    'yellow': '#FFD700',
    'deep_blue': '#0A0E27',
    'dark_gray': '#1A1A2E'
}


def get_neon_theme() -> Dict:
    """
    Return Plotly layout configuration for neon/cyberpunk theme.
    
    Returns:
        Dictionary with plot layout settings (without title, xaxis, yaxis)
    """
    return {
        'plot_bgcolor': 'rgba(0,0,0,0)',  # Transparent background
        'paper_bgcolor': 'rgba(15, 23, 42, 0.3)',  # Semi-transparent dark blue
        'font': {
            'family': 'Inter, Segoe UI, sans-serif',
            'size': 12,
            'color': '#e2e8f0'
        },
        'hovermode': 'x unified',
        'hoverlabel': {
            'bgcolor': 'rgba(30, 41, 59, 0.95)',
            'font_size': 12,
            'font_family': 'Inter, Segoe UI, sans-serif',
            'bordercolor': CHART_COLORS['green']
        }
    }


def get_default_axis_style() -> Dict:
    """
    Return default axis styling for charts.
    
    Returns:
        Dictionary with xaxis and yaxis configurations
    """
    return {
        'xaxis': {
            'gridcolor': 'rgba(57, 255, 20, 0.1)',
            'showgrid': True,
            'zeroline': False,
            'color': '#94a3b8',
            'tickfont': {'size': 10}
        },
        'yaxis': {
            'gridcolor': 'rgba(0, 240, 255, 0.1)',
            'showgrid': True,
            'zeroline': False,
            'color': '#94a3b8',
            'tickfont': {'size': 10}
        }
    }


def render_dashboard_charts(df: pd.DataFrame) -> Tuple[go.Figure, go.Figure, go.Figure]:
    """
    Create three main dashboard charts with neon styling.
    
    Args:
        df: DataFrame with daily log data
    
    Returns:
        Tuple of three Plotly Figure objects:
        1. Bio-Rhythm Chart (sleep, energy, mood)
        2. Focus Chart (study hours, focus score, screen time)
        3. Cognitive Chart (PVT, recall, total index)
    
    Examples:
        >>> from modules.data_manager import DataManager
        >>> dm = DataManager()
        >>> df = dm.get_mock_data(7)
        >>> bio_fig, focus_fig, cog_fig = render_dashboard_charts(df)
        >>> bio_fig.show()
    """
    # Handle empty DataFrame
    if df.empty:
        empty_fig = create_empty_chart("No data available")
        return empty_fig, empty_fig, empty_fig
    
    # Ensure date column is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
    
    # Create three charts
    bio_rhythm_fig = create_bio_rhythm_chart(df)
    focus_fig = create_focus_chart(df)
    cognitive_fig = create_cognitive_chart(df)
    
    return bio_rhythm_fig, focus_fig, cognitive_fig


def create_bio_rhythm_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create Bio-Rhythm chart showing sleep, energy, and mood patterns.
    
    Args:
        df: DataFrame with bio-rhythm data
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Sleep hours (converted to 0-10 scale for comparison)
    if 'sleep_hours' in df.columns and 'date' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['sleep_hours'],
            name='Sleep Hours',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['cyan'], width=3, shape='spline'),
            marker=dict(size=8, symbol='circle', line=dict(width=2, color='white')),
            hovertemplate='<b>Sleep</b>: %{y:.1f} hrs<extra></extra>',
            fill='tozeroy',
            fillcolor='rgba(0, 240, 255, 0.1)'
        ))
    
    # Sleep quality (0-10 scale)
    if 'sleep_quality' in df.columns and 'date' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['sleep_quality'],
            name='Sleep Quality',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['purple'], width=2, dash='dot'),
            marker=dict(size=6, symbol='diamond'),
            hovertemplate='<b>Quality</b>: %{y}/10<extra></extra>'
        ))
    
    # Energy level (0-10 scale)
    if 'energy_level' in df.columns and 'date' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['energy_level'],
            name='Energy Level',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['green'], width=3, shape='spline'),
            marker=dict(size=8, symbol='star'),
            hovertemplate='<b>Energy</b>: %{y}/10<extra></extra>'
        ))
    
    # Mood (0-10 scale)
    if 'mood' in df.columns and 'date' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['mood'],
            name='Mood',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['pink'], width=2),
            marker=dict(size=7, symbol='circle'),
            hovertemplate='<b>Mood</b>: %{y}/10<extra></extra>'
        ))
    
    # Apply neon theme
    theme = get_neon_theme()
    axis_style = get_default_axis_style()
    fig.update_layout(
        **theme,
        title=dict(
            text='🌙 Bio-Rhythm Analysis',
            font=dict(
                size=18,
                color=CHART_COLORS['cyan'],
                family='Inter, Segoe UI, sans-serif'
            ),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            **axis_style['xaxis'],
            title='Date'
        ),
        yaxis=dict(
            **axis_style['yaxis'],
            title='Score / Hours'
        ),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.15,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(30, 41, 59, 0.6)',
            bordercolor=CHART_COLORS['cyan'],
            borderwidth=1
        ),
        height=450,
        margin={'l': 50, 'r': 30, 't': 60, 'b': 80}
    )
    
    return fig


def create_focus_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create Focus chart showing study hours, focus score, and screen time.
    
    Args:
        df: DataFrame with focus-related data
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Study hours
    if 'study_hours' in df.columns and 'date' in df.columns:
        fig.add_trace(go.Bar(
            x=df['date'],
            y=df['study_hours'],
            name='Study Hours',
            marker=dict(
                color=df['study_hours'] if 'study_hours' in df.columns else CHART_COLORS['green'],
                colorscale=[[0, CHART_COLORS['purple']], [0.5, CHART_COLORS['cyan']], [1, CHART_COLORS['green']]],
                line=dict(color=CHART_COLORS['green'], width=1),
                opacity=0.8
            ),
            hovertemplate='<b>Study</b>: %{y:.1f} hrs<extra></extra>',
            yaxis='y'
        ))
    
    # Focus score (0-10 scale)
    if 'focus_score' in df.columns and 'date' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['focus_score'],
            name='Focus Score',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['cyan'], width=3, shape='spline'),
            marker=dict(size=10, symbol='diamond', line=dict(width=2, color='white')),
            hovertemplate='<b>Focus</b>: %{y}/10<extra></extra>',
            yaxis='y2'
        ))
    
    # Screen time (inverted - less is better)
    if 'screen_time_hours' in df.columns and 'date' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['screen_time_hours'],
            name='Screen Time',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['orange'], width=2, dash='dash'),
            marker=dict(size=6, symbol='x'),
            hovertemplate='<b>Screen</b>: %{y:.1f} hrs<extra></extra>',
            yaxis='y'
        ))
    
    # Apply neon theme with dual y-axes
    theme = get_neon_theme()
    fig.update_layout(
        **theme,
        title=dict(
            text='🎯 Focus & Productivity Analysis',
            font=dict(
                size=18,
                color=CHART_COLORS['cyan'],
                family='Inter, Segoe UI, sans-serif'
            ),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Date',
            gridcolor='rgba(57, 255, 20, 0.1)',
            showgrid=True,
            zeroline=False,
            color='#94a3b8',
            tickfont={'size': 10}
        ),
        yaxis=dict(
            title=dict(
                text='Hours',
                font=dict(color=CHART_COLORS['green'])
            ),
            tickfont=dict(color=CHART_COLORS['green']),
            gridcolor='rgba(57, 255, 20, 0.1)',
            showgrid=True,
            zeroline=False
        ),
        yaxis2=dict(
            title=dict(
                text='Score (0-10)',
                font=dict(color=CHART_COLORS['cyan'])
            ),
            tickfont=dict(color=CHART_COLORS['cyan']),
            overlaying='y',
            side='right',
            gridcolor='rgba(0, 240, 255, 0.1)',
            showgrid=False
        ),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.15,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(30, 41, 59, 0.6)',
            bordercolor=CHART_COLORS['cyan'],
            borderwidth=1
        ),
        height=450,
        margin={'l': 50, 'r': 50, 't': 60, 'b': 80},
        barmode='overlay'
    )
    
    return fig


def create_cognitive_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create Cognitive Performance chart showing PVT, recall, and total index.
    
    Args:
        df: DataFrame with cognitive metrics
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Total Index (primary metric, 0-100 scale)
    if 'total_index' in df.columns and 'date' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['total_index'],
            name='Total Index',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['green'], width=4, shape='spline'),
            marker=dict(
                size=12, 
                symbol='circle',
                line=dict(width=2, color='white'),
                gradient=dict(type='radial', color=CHART_COLORS['cyan'])
            ),
            hovertemplate='<b>Total Index</b>: %{y}<extra></extra>',
            fill='tozeroy',
            fillcolor='rgba(57, 255, 20, 0.15)'
        ))
    
    # Recall percentage (0-100 scale)
    if 'recall_percent' in df.columns and 'date' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['recall_percent'],
            name='Recall %',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['purple'], width=2, dash='dot'),
            marker=dict(size=8, symbol='square'),
            hovertemplate='<b>Recall</b>: %{y}%<extra></extra>'
        ))
    
    # PVT Score (inverted - converted to 0-100 scale for visualization)
    # Lower PVT ms = better, so invert for display
    if 'pvt_avg_ms' in df.columns and 'date' in df.columns:
        # Convert PVT to score: 100 = 200ms (excellent), 0 = 1000ms (poor)
        pvt_score = 100 - ((df['pvt_avg_ms'] - 200) / 8).clip(0, 100)
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=pvt_score,
            name='PVT Score',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['cyan'], width=2),
            marker=dict(size=8, symbol='diamond'),
            hovertemplate='<b>PVT</b>: %{text}<extra></extra>',
            text=[f"{ms}ms" for ms in df['pvt_avg_ms']],
            customdata=df['pvt_avg_ms']
        ))
    
    # Add reference lines for performance categories
    fig.add_hline(
        y=90, line_dash="dash", line_color=CHART_COLORS['green'], 
        opacity=0.3, annotation_text="Elite (90+)", 
        annotation_position="right"
    )
    fig.add_hline(
        y=70, line_dash="dash", line_color=CHART_COLORS['yellow'], 
        opacity=0.3, annotation_text="Good (70+)", 
        annotation_position="right"
    )
    
    # Apply neon theme
    theme = get_neon_theme()
    axis_style = get_default_axis_style()
    fig.update_layout(
        **theme,
        title=dict(
            text='🧠 Cognitive Performance Index',
            font=dict(
                size=18,
                color=CHART_COLORS['cyan'],
                family='Inter, Segoe UI, sans-serif'
            ),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            **axis_style['xaxis'],
            title='Date'
        ),
        yaxis=dict(
            **axis_style['yaxis'],
            title='Score / Percentage',
            range=[0, 105]
        ),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.15,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(30, 41, 59, 0.6)',
            bordercolor=CHART_COLORS['green'],
            borderwidth=1
        ),
        height=450,
        margin={'l': 50, 'r': 30, 't': 60, 'b': 80}
    )
    
    return fig


def create_empty_chart(message: str = "No data available") -> go.Figure:
    """
    Create an empty chart with a message.
    
    Args:
        message: Message to display
    
    Returns:
        Empty Plotly Figure
    """
    fig = go.Figure()
    
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color=CHART_COLORS['cyan'])
    )
    
    theme = get_neon_theme()
    fig.update_layout(
        **theme,
        title=dict(
            text=message,
            font=dict(
                size=18,
                color=CHART_COLORS['cyan'],
                family='Inter, Segoe UI, sans-serif'
            ),
            x=0.5,
            xanchor='center'
        ),
        height=400,
        margin={'l': 50, 'r': 30, 't': 50, 'b': 50}
    )
    
    return fig


# Export all chart functions
__all__ = [
    'render_dashboard_charts',
    'create_bio_rhythm_chart',
    'create_focus_chart',
    'create_cognitive_chart',
    'create_empty_chart',
    'get_neon_theme'
]
