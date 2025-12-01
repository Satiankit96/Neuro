"""
Simple CSV-based data persistence for UPSC Neuro-OS
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime, time, timedelta, date
from typing import Optional, Dict, Any
from utils.scoring import calculate_total_index


class DataManager:
    """Manages saving and loading of daily productivity logs."""
    
    def __init__(self, filepath: str = "upsc_logs.csv"):
        """
        Initialize DataManager.
        
        Args:
            filepath: Path to CSV file for storing logs
        """
        self.filepath = Path(filepath)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create CSV file with headers if it doesn't exist."""
        if not self.filepath.exists():
            columns = [
                'date',
                'study_hours',
                'screen_time_minutes',
                'recall_percent',
                'sleep_hours',
                'bedtime',
                'wake_time',
                'diet_quality',
                'exercise_minutes',
                'sunlight_minutes',
                'cycle_day',
                'study_score',
                'recall_score',
                'sleep_score',
                'diet_score',
                'exercise_score',
                'sunlight_score',
                'circadian_penalty',
                'distraction_penalty',
                'total_index',
                'cognitive_roi'
            ]
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.filepath, index=False)
    
    def save_entry(self, entry: dict):
        """
        Save a daily entry to CSV.
        
        Args:
            entry: Dictionary with all entry data
        """
        df = pd.read_csv(self.filepath)
        
        # Convert date to string if it's a date object
        if isinstance(entry.get('date'), datetime):
            entry['date'] = entry['date'].strftime('%Y-%m-%d')
        
        # Convert time objects to strings
        if isinstance(entry.get('bedtime'), time):
            entry['bedtime'] = entry['bedtime'].strftime('%H:%M:%S')
        if isinstance(entry.get('wake_time'), time):
            entry['wake_time'] = entry['wake_time'].strftime('%H:%M:%S')
        
        # Check if entry for this date already exists
        if entry['date'] in df['date'].values:
            # Remove old entry and add new one
            df = df[df['date'] != entry['date']]
            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        else:
            # Append new entry
            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        
        # Sort by date descending
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        # Save to CSV
        df.to_csv(self.filepath, index=False)
    
    def load_data(self) -> pd.DataFrame:
        """
        Load all data from CSV.
        
        Returns:
            DataFrame with all entries
        """
        if not self.filepath.exists():
            return pd.DataFrame()
        
        df = pd.read_csv(self.filepath)
        
        if df.empty:
            return df
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Convert time columns back to time objects for processing
        if 'bedtime' in df.columns:
            df['bedtime'] = pd.to_datetime(df['bedtime'], format='%H:%M:%S').dt.time
        if 'wake_time' in df.columns:
            df['wake_time'] = pd.to_datetime(df['wake_time'], format='%H:%M:%S').dt.time
        
        return df
    
    def get_latest_entry(self) -> Optional[dict]:
        """
        Get the most recent entry.
        
        Returns:
            Dictionary with latest entry, or None if no data
        """
        df = self.load_data()
        if df.empty:
            return None
        
        latest = df.iloc[0].to_dict()
        return latest
    
    def get_entry_by_date(self, date: str) -> Optional[dict]:
        """
        Get entry for a specific date.
        
        Args:
            date: Date string in format 'YYYY-MM-DD'
        
        Returns:
            Dictionary with entry data, or None if not found
        """
        df = self.load_data()
        if df.empty:
            return None
        
        df['date'] = pd.to_datetime(df['date'])
        target_date = pd.to_datetime(date)
        
        entry = df[df['date'] == target_date]
        if entry.empty:
            return None
        
        return entry.iloc[0].to_dict()
    
    def generate_dummy_data(self, days: int = 120):
        """
        Generate realistic dummy data for testing.
        
        Args:
            days: Number of days of data to generate (default: 120 for 4 months)
        """
        np.random.seed(42)  # For reproducible results
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days - 1)
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            
            # Generate realistic values with some variation
            study_hours = np.random.uniform(4.0, 9.0)
            screen_time_minutes = int(np.random.uniform(30, 180))
            recall_percent = np.random.uniform(65, 95)
            sleep_hours = np.random.uniform(6.0, 8.5)
            
            # Bedtime variation (21:30 to 00:30)
            bedtime_hour = np.random.randint(21, 24)
            bedtime_minute = np.random.choice([0, 15, 30, 45])
            if bedtime_hour == 24:
                bedtime_hour = 0
            bedtime = time(bedtime_hour, bedtime_minute)
            
            # Wake time variation (05:00 to 07:30)
            wake_hour = np.random.randint(5, 8)
            wake_minute = np.random.choice([0, 15, 30, 45])
            if wake_hour == 8:
                wake_minute = 0
            wake_time = time(wake_hour, wake_minute)
            
            diet_quality = int(np.random.uniform(5, 10))
            exercise_minutes = int(np.random.uniform(20, 90))
            sunlight_minutes = int(np.random.uniform(15, 120))
            cycle_day = int(np.random.uniform(1, 29))
            
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
            
            # Create entry
            entry = {
                'date': current_date,
                'study_hours': round(study_hours, 1),
                'screen_time_minutes': screen_time_minutes,
                'recall_percent': round(recall_percent, 1),
                'sleep_hours': round(sleep_hours, 1),
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
            self.save_entry(entry)
        
        print(f"✅ Generated {days} days of dummy data from {start_date} to {end_date}")


class UserConfigManager:
    """Manages user settings persistence via JSON."""
    
    def __init__(self, filepath: str = "data/user_config.json"):
        """
        Initialize UserConfigManager.
        
        Args:
            filepath: Path to JSON file for storing user config
        """
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create JSON file with defaults if it doesn't exist."""
        if not self.filepath.exists():
            default_config = {
                'last_period_date': None
            }
            self._save_config(default_config)
    
    def _save_config(self, config: Dict[str, Any]):
        """Save config to JSON file."""
        with open(self.filepath, 'w') as f:
            json.dump(config, f, indent=2, default=str)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load config from JSON file."""
        with open(self.filepath, 'r') as f:
            return json.load(f)
    
    def get_last_period_date(self) -> Optional[date]:
        """Get the last period date from config."""
        config = self._load_config()
        date_str = config.get('last_period_date')
        if date_str:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        return None
    
    def set_last_period_date(self, period_date: date):
        """Save the last period date to config."""
        config = self._load_config()
        config['last_period_date'] = period_date.strftime('%Y-%m-%d')
        self._save_config(config)
    
    def calculate_cycle_day(self, current_date: Optional[date] = None) -> int:
        """
        Calculate the current cycle day based on last period date.
        
        Args:
            current_date: Date to calculate for (defaults to today)
        
        Returns:
            Cycle day (1-28), or 14 if no period date set
        """
        if current_date is None:
            current_date = datetime.now().date()
        
        last_period = self.get_last_period_date()
        if last_period is None:
            return 14  # Default to mid-cycle
        
        days_diff = (current_date - last_period).days
        return (days_diff % 28) + 1
    
    def get_cycle_phase(self, cycle_day: int) -> str:
        """
        Get the cycle phase name for a given cycle day.
        
        Args:
            cycle_day: Day of the cycle (1-28)
        
        Returns:
            Phase name
        """
        if 1 <= cycle_day <= 5:
            return "Menstrual Phase"
        elif 6 <= cycle_day <= 13:
            return "Follicular Phase"
        elif 14 <= cycle_day <= 16:
            return "Ovulation Phase"
        else:
            return "Luteal Phase"

