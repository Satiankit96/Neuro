"""
UPSC Neuro-OS Configuration Settings
=====================================
Central configuration file for all constants, theme colors, file paths, and scoring parameters.
"""

import os
from pathlib import Path

# ==================== PROJECT PATHS ====================
# Base directory of the project
BASE_DIR = Path(__file__).parent.parent

# Data storage paths
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Database/CSV file paths
DAILY_LOG_FILE = DATA_DIR / "daily_logs.csv"
PVT_RESULTS_FILE = DATA_DIR / "pvt_results.csv"
ANALYTICS_FILE = DATA_DIR / "analytics.csv"


# ==================== THEME COLORS ====================
# Neon/Cyberpunk theme colors
NEON_GREEN = "#39FF14"
DEEP_BLUE = "#0A0E27"
ELECTRIC_PURPLE = "#BF00FF"
CYBER_CYAN = "#00F0FF"
DARK_GRAY = "#1A1A2E"
ACCENT_PINK = "#FF006E"

# Color palette dictionary for easy access
THEME_COLORS = {
    "primary": NEON_GREEN,
    "background": DEEP_BLUE,
    "secondary": ELECTRIC_PURPLE,
    "accent": CYBER_CYAN,
    "dark": DARK_GRAY,
    "highlight": ACCENT_PINK
}


# ==================== SCORING & METRICS ====================
# Maximum scores for various parameters
MAX_SCORES = {
    "sleep_quality": 10,
    "study_hours": 16,
    "exercise_minutes": 120,
    "meditation_minutes": 60,
    "mood": 10,
    "focus_score": 10,
    "energy_level": 10,
    "stress_level": 10,
    "pvt_reaction_time_ms": 500  # Lower is better
}

# Minimum acceptable scores
MIN_SCORES = {
    "sleep_quality": 0,
    "study_hours": 0,
    "exercise_minutes": 0,
    "meditation_minutes": 0,
    "mood": 0,
    "focus_score": 0,
    "energy_level": 0,
    "stress_level": 0,
    "pvt_reaction_time_ms": 100  # Lower bound for realistic reaction time
}


# ==================== PVT GAME SETTINGS ====================
PVT_CONFIG = {
    "num_trials": 10,
    "min_wait_time_ms": 2000,
    "max_wait_time_ms": 5000,
    "trial_timeout_ms": 3000,
    "warning_threshold_ms": 300  # Flag if reaction time > 300ms
}


# ==================== APP SETTINGS ====================
APP_TITLE = "UPSC Neuro-OS"
APP_ICON = "🧠"
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}


# ==================== DATA VALIDATION ====================
REQUIRED_COLUMNS = [
    "date",
    "sleep_hours",
    "sleep_quality",
    "study_hours",
    "exercise_minutes",
    "meditation_minutes",
    "mood",
    "focus_score",
    "energy_level",
    "stress_level",
    "water_intake_liters",
    "screen_time_hours",
    "notes"
]


# ==================== EXPORT SETTINGS ====================
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
