"""
UPSC Neuro-OS Style Loader
===========================
Utility module for loading and injecting CSS styles into Streamlit.
Keeps styling logic separate from UI components.

Author: Senior Python Software Architect
Date: November 29, 2025
"""

import streamlit as st
from pathlib import Path
from typing import Optional


def load_css(css_file: Optional[Path] = None) -> None:
    """
    Load and inject CSS styles into the Streamlit app.
    
    Reads CSS from assets/style.css and injects it using st.markdown
    with unsafe_allow_html=True for custom styling.
    
    Args:
        css_file: Path to CSS file (defaults to assets/style.css)
    
    Examples:
        >>> from ui.style_loader import load_css
        >>> load_css()  # Loads default style.css
        >>> load_css(Path("custom.css"))  # Load custom CSS
    
    Notes:
        - Call this once at the top of your Streamlit app
        - CSS is scoped to the current session
        - Supports glassmorphism, neon effects, and dark mode
    """
    # Default to assets/style.css
    if css_file is None:
        base_dir = Path(__file__).parent.parent
        css_file = base_dir / "assets" / "style.css"
    
    # Check if file exists
    if not css_file.exists():
        st.warning(f"⚠️ CSS file not found: {css_file}")
        return
    
    try:
        # Read CSS content
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Inject CSS into Streamlit
        st.markdown(
            f"<style>{css_content}</style>",
            unsafe_allow_html=True
        )
        
        # Optional: Add success indicator in debug mode
        # st.success("✅ Custom CSS loaded successfully")
    
    except Exception as e:
        st.error(f"❌ Error loading CSS: {e}")


def apply_glassmorphism(content: str, container_class: str = "glass-container") -> str:
    """
    Wrap content in a glassmorphism container.
    
    Args:
        content: HTML content to wrap
        container_class: CSS class for the container (glass-container, glass-card, glass-panel)
    
    Returns:
        HTML string with glassmorphism wrapper
    
    Examples:
        >>> html = apply_glassmorphism("<h1>Hello</h1>")
        >>> st.markdown(html, unsafe_allow_html=True)
    """
    return f'<div class="{container_class}">{content}</div>'


def neon_text(text: str, color: str = "green") -> str:
    """
    Create neon text effect.
    
    Args:
        text: Text content
        color: Neon color ('green', 'cyan', 'purple', 'pink')
    
    Returns:
        HTML string with neon text styling
    
    Examples:
        >>> html = neon_text("UPSC Neuro-OS", "cyan")
        >>> st.markdown(html, unsafe_allow_html=True)
    """
    color_classes = {
        "green": "neon-text",
        "cyan": "neon-text-cyan",
        "purple": "neon-text-purple",
        "pink": "neon-text-pink"
    }
    
    css_class = color_classes.get(color.lower(), "neon-text")
    return f'<span class="{css_class}">{text}</span>'


def neon_heading(text: str, level: int = 1, color: str = "green") -> str:
    """
    Create neon heading (h1-h6).
    
    Args:
        text: Heading text
        level: Heading level (1-6)
        color: Neon color
    
    Returns:
        HTML heading with neon effect
    
    Examples:
        >>> html = neon_heading("Dashboard", level=2, color="cyan")
        >>> st.markdown(html, unsafe_allow_html=True)
    """
    level = max(1, min(6, level))  # Clamp to 1-6
    neon_html = neon_text(text, color)
    return f'<h{level}>{neon_html}</h{level}>'


def gradient_text(text: str) -> str:
    """
    Create gradient text effect (green -> cyan -> purple).
    
    Args:
        text: Text content
    
    Returns:
        HTML with gradient text styling
    
    Examples:
        >>> html = gradient_text("Performance Index: 92")
        >>> st.markdown(html, unsafe_allow_html=True)
    """
    return f'<span class="text-gradient">{text}</span>'


def glow_box(content: str) -> str:
    """
    Wrap content in a glowing box.
    
    Args:
        content: HTML content
    
    Returns:
        HTML with glow effect
    """
    return f'<div class="glow-box glass-card">{content}</div>'


def fade_in(content: str) -> str:
    """
    Apply fade-in animation to content.
    
    Args:
        content: HTML content
    
    Returns:
        HTML with fade-in animation
    """
    return f'<div class="fade-in">{content}</div>'


def inject_custom_html(html: str) -> None:
    """
    Safely inject custom HTML into Streamlit.
    
    Args:
        html: HTML string to inject
    
    Examples:
        >>> inject_custom_html('<div class="glass-container">Content</div>')
    """
    st.markdown(html, unsafe_allow_html=True)


# Convenience function for common styling patterns
def styled_metric(label: str, value: str, delta: Optional[str] = None) -> str:
    """
    Create a styled metric card with glassmorphism and neon effects.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta/change indicator
    
    Returns:
        HTML string for styled metric
    
    Examples:
        >>> html = styled_metric("Sleep Score", "20/20", "+2")
        >>> inject_custom_html(html)
    """
    delta_html = f'<div style="color: #39FF14; font-size: 0.9rem;">{delta}</div>' if delta else ''
    
    html = f'''
    <div class="glass-card" style="text-align: center; margin: 10px 0;">
        <div class="neon-text-cyan" style="font-size: 0.9rem; margin-bottom: 8px;">{label}</div>
        <div class="neon-text" style="font-size: 2rem; font-weight: 700;">{value}</div>
        {delta_html}
    </div>
    '''
    return html


def create_header(title: str, subtitle: Optional[str] = None) -> str:
    """
    Create a styled header with optional subtitle.
    
    Args:
        title: Main title
        subtitle: Optional subtitle
    
    Returns:
        HTML string for header
    """
    subtitle_html = f'<div class="neon-subtitle" style="margin-top: 8px; font-size: 1.1rem;">{subtitle}</div>' if subtitle else ''
    
    html = f'''
    <div class="fade-in" style="text-align: center; margin-bottom: 30px;">
        <h1 class="neon-text" style="font-size: 3rem; margin-bottom: 0;">🧠 {title}</h1>
        {subtitle_html}
    </div>
    '''
    return html


# Export all public functions
__all__ = [
    'load_css',
    'apply_glassmorphism',
    'neon_text',
    'neon_heading',
    'gradient_text',
    'glow_box',
    'fade_in',
    'inject_custom_html',
    'styled_metric',
    'create_header'
]
