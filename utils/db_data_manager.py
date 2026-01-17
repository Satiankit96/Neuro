"""
PostgreSQL-based data persistence for Neuro Index
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta, date
from typing import Optional, Dict, Any
from sqlalchemy import desc
from utils.database import get_session, DailyEntry, UserConfig
from utils.scoring import calculate_total_index, calculate_cognitive_roi


class DataManager:
    """Manages saving and loading of daily productivity logs using PostgreSQL."""
    
    def __init__(self, filepath: str = None):
        """
        Initialize DataManager.
        
        Args:
            filepath: Ignored (kept for compatibility with old CSV version)
        """
        pass
    
    def save_entry(self, entry: dict):
        """
        Save a daily entry to database.
        
        Args:
            entry: Dictionary with all entry data
        """
        session = get_session()
        try:
            # Convert date to date object if it's datetime
            entry_date = entry.get('date')
            if isinstance(entry_date, datetime):
                entry_date = entry_date.date()
            elif isinstance(entry_date, str):
                entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
            
            # Check if entry for this date already exists
            existing = session.query(DailyEntry).filter_by(date=entry_date).first()
            
            if existing:
                # Update existing entry
                for key, value in entry.items():
                    if key != 'date' and hasattr(existing, key):
                        setattr(existing, key, value)
            else:
                # Create new entry
                new_entry = DailyEntry(
                    date=entry_date,
                    study_hours=entry['study_hours'],
                    screen_time_minutes=entry['screen_time_minutes'],
                    recall_percent=entry['recall_percent'],
                    sleep_hours=entry['sleep_hours'],
                    bedtime=entry['bedtime'],
                    wake_time=entry['wake_time'],
                    diet_quality=entry['diet_quality'],
                    exercise_minutes=entry['exercise_minutes'],
                    sunlight_minutes=entry.get('sunlight_minutes', 0),
                    cycle_day=entry['cycle_day'],
                    study_score=entry['study_score'],
                    recall_score=entry['recall_score'],
                    sleep_score=entry['sleep_score'],
                    diet_score=entry['diet_score'],
                    exercise_score=entry['exercise_score'],
                    sunlight_score=entry.get('sunlight_score', 0),
                    circadian_penalty=entry['circadian_penalty'],
                    distraction_penalty=entry['distraction_penalty'],
                    total_index=entry['total_index'],
                    cognitive_roi=entry['cognitive_roi']
                )
                session.add(new_entry)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def load_data(self) -> pd.DataFrame:
        """
        Load all data from database.
        
        Returns:
            DataFrame with all entries
        """
        session = get_session()
        try:
            entries = session.query(DailyEntry).order_by(desc(DailyEntry.date)).all()
            
            if not entries:
                return pd.DataFrame()
            
            # Convert to DataFrame
            data = [entry.to_dict() for entry in entries]
            df = pd.DataFrame(data)
            
            # Ensure date column is datetime
            df['date'] = pd.to_datetime(df['date'])
            
            return df
        finally:
            session.close()
    
    def get_latest_entry(self) -> Optional[dict]:
        """
        Get the most recent entry.
        
        Returns:
            Dictionary with latest entry data, or None if no entries
        """
        session = get_session()
        try:
            entry = session.query(DailyEntry).order_by(desc(DailyEntry.date)).first()
            return entry.to_dict() if entry else None
        finally:
            session.close()
    
    def generate_dummy_data(self, days: int = 120):
        """
        Generate dummy data for testing (sequential dates from today backwards).
        
        Args:
            days: Number of days to generate (default 120 = 4 months)
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        print(f"Generating {days} days of dummy data...")
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            
            # Generate realistic random data
            study_hours = np.random.uniform(2, 10)
            screen_time_minutes = int(np.random.uniform(30, 240))
            recall_percent = np.random.uniform(40, 95)
            sleep_hours = np.random.uniform(5, 9)
            
            # Generate bedtime (21:00 to 01:00)
            bedtime_hour = np.random.choice([21, 22, 23, 0, 1])
            bedtime_minute = np.random.choice([0, 15, 30, 45])
            bedtime = time(bedtime_hour, bedtime_minute)
            
            # Generate wake time (05:00 to 08:00)
            wake_hour = np.random.choice([5, 6, 7, 8])
            wake_minute = np.random.choice([0, 15, 30, 45])
            wake_time = time(wake_hour, wake_minute)
            
            diet_quality = int(np.random.uniform(4, 10))
            exercise_minutes = int(np.random.uniform(0, 90))
            sunlight_minutes = int(np.random.uniform(0, 60))
            
            # Cycle day (1-28)
            cycle_day = ((i % 28) + 1)
            
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
    """Manages user settings persistence via PostgreSQL."""
    
    def __init__(self, filepath: str = None):
        """
        Initialize UserConfigManager.
        
        Args:
            filepath: Ignored (kept for compatibility)
        """
        pass
    
    def get_last_period_date(self) -> Optional[date]:
        """Get the last period date from config."""
        session = get_session()
        try:
            config = session.query(UserConfig).filter_by(key='last_period_date').first()
            if config and config.value:
                return datetime.strptime(config.value, '%Y-%m-%d').date()
            return None
        finally:
            session.close()
    
    def set_last_period_date(self, period_date: date):
        """Save the last period date to config."""
        session = get_session()
        try:
            config = session.query(UserConfig).filter_by(key='last_period_date').first()
            
            if config:
                config.value = period_date.strftime('%Y-%m-%d')
            else:
                config = UserConfig(
                    key='last_period_date',
                    value=period_date.strftime('%Y-%m-%d')
                )
                session.add(config)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
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
