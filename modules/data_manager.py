"""
UPSC Neuro-OS Data Persistence Layer
=====================================
Handles all data storage, retrieval, and CSV operations.
Separates data logic from UI and business logic.

Author: Senior Python Software Architect
Date: November 29, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import json

# Import project settings
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import (
    DAILY_LOG_FILE, 
    PVT_RESULTS_FILE, 
    ANALYTICS_FILE,
    REQUIRED_COLUMNS,
    DATE_FORMAT,
    DATETIME_FORMAT
)


class DataManager:
    """
    Manages data persistence for UPSC Neuro-OS application.
    
    Responsibilities:
    - Load/save daily logs to CSV
    - Generate mock data for testing
    - Validate data integrity
    - Handle file I/O errors gracefully
    """
    
    def __init__(self, data_file: Optional[Path] = None):
        """
        Initialize DataManager with specified data file path.
        
        Args:
            data_file: Path to CSV file (defaults to DAILY_LOG_FILE from config)
        """
        self.data_file = data_file or DAILY_LOG_FILE
        self.pvt_file = PVT_RESULTS_FILE
        self.analytics_file = ANALYTICS_FILE
        
        # Ensure parent directory exists
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_data(self) -> pd.DataFrame:
        """
        Load daily log data from CSV file.
        
        If file doesn't exist, returns an empty DataFrame with correct schema.
        Handles corrupted files by backing up and starting fresh.
        
        Returns:
            DataFrame with columns matching REQUIRED_COLUMNS
        
        Examples:
            >>> dm = DataManager()
            >>> df = dm.load_data()
            >>> print(df.columns.tolist())
            ['date', 'sleep_hours', 'sleep_quality', ...]
        """
        # Define the schema for daily logs
        schema = {
            'date': 'object',
            'sleep_hours': 'float64',
            'sleep_quality': 'int64',
            'bedtime': 'object',
            'wake_time': 'object',
            'study_hours': 'float64',
            'exercise_minutes': 'int64',
            'meditation_minutes': 'int64',
            'diet_quality': 'int64',
            'recall_percent': 'int64',
            'pvt_avg_ms': 'int64',
            'mood': 'int64',
            'focus_score': 'int64',
            'energy_level': 'int64',
            'stress_level': 'int64',
            'water_intake_liters': 'float64',
            'screen_time_hours': 'float64',
            'notes': 'object',
            'total_index': 'int64'
        }
        
        if not self.data_file.exists():
            # Create empty DataFrame with correct schema
            df = pd.DataFrame(columns=schema.keys())
            for col, dtype in schema.items():
                df[col] = df[col].astype(dtype)
            return df
        
        try:
            df = pd.read_csv(self.data_file, parse_dates=['date'])
            
            # Validate columns
            missing_cols = set(schema.keys()) - set(df.columns)
            if missing_cols:
                print(f"Warning: Missing columns {missing_cols}. Adding them...")
                for col in missing_cols:
                    df[col] = None
            
            # Ensure correct data types
            for col, dtype in schema.items():
                if col in df.columns:
                    try:
                        if dtype == 'object':
                            df[col] = df[col].astype(str).replace('nan', '')
                        else:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    except Exception as e:
                        print(f"Warning: Could not convert {col} to {dtype}: {e}")
            
            return df
        
        except Exception as e:
            print(f"Error loading data from {self.data_file}: {e}")
            # Backup corrupted file
            backup_path = self.data_file.with_suffix('.csv.backup')
            if self.data_file.exists():
                self.data_file.rename(backup_path)
                print(f"Corrupted file backed up to {backup_path}")
            
            # Return empty DataFrame
            df = pd.DataFrame(columns=schema.keys())
            for col, dtype in schema.items():
                df[col] = df[col].astype(dtype)
            return df
    
    def save_entry(self, entry: Dict) -> bool:
        """
        Save a new daily log entry to CSV file.
        
        Appends the entry to existing data or creates new file if needed.
        Validates entry data before saving.
        
        Args:
            entry: Dictionary containing daily log fields
        
        Returns:
            True if save successful, False otherwise
        
        Raises:
            ValueError: If required fields are missing
        
        Examples:
            >>> dm = DataManager()
            >>> entry = {
            ...     'date': '2025-11-29',
            ...     'sleep_hours': 7.5,
            ...     'sleep_quality': 8,
            ...     'total_index': 85
            ... }
            >>> dm.save_entry(entry)
            True
        """
        # Validate required fields
        required_fields = ['date', 'sleep_hours', 'sleep_quality']
        missing_fields = [f for f in required_fields if f not in entry]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        try:
            # Load existing data
            df = self.load_data()
            
            # Create new entry DataFrame
            new_entry = pd.DataFrame([entry])
            
            # Ensure date is properly formatted
            if 'date' in new_entry.columns:
                new_entry['date'] = pd.to_datetime(new_entry['date']).dt.strftime(DATE_FORMAT)
            
            # Check for duplicate date
            if not df.empty and 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.strftime(DATE_FORMAT)
                
                if entry['date'] in df['date'].values:
                    # Update existing entry
                    df = df[df['date'] != entry['date']]
                    print(f"Updating existing entry for {entry['date']}")
            
            # Append new entry
            df = pd.concat([df, new_entry], ignore_index=True)
            
            # Sort by date (most recent first)
            df = df.sort_values('date', ascending=False)
            
            # Save to CSV
            df.to_csv(self.data_file, index=False)
            print(f"✅ Entry saved successfully to {self.data_file}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error saving entry: {e}")
            return False
    
    def get_mock_data(self, num_days: int = 7) -> pd.DataFrame:
        """
        Generate realistic mock data for testing purposes.
        
        Creates a DataFrame with {num_days} days of simulated daily logs,
        with realistic variations in sleep, study, exercise, and cognitive metrics.
        
        Args:
            num_days: Number of days of mock data to generate (default: 7)
        
        Returns:
            DataFrame with mock daily log entries
        
        Examples:
            >>> dm = DataManager()
            >>> mock_df = dm.get_mock_data(7)
            >>> print(len(mock_df))
            7
            >>> print(mock_df['sleep_hours'].mean())
            ~7.2
        """
        np.random.seed(42)  # For reproducibility
        
        mock_entries = []
        base_date = datetime.now() - timedelta(days=num_days - 1)
        
        for i in range(num_days):
            current_date = base_date + timedelta(days=i)
            
            # Realistic sleep patterns (6-9 hours, trending towards 7-8)
            sleep_hours = np.clip(np.random.normal(7.2, 0.8), 5.5, 9.5)
            sleep_quality = int(np.clip(np.random.normal(7, 1.5), 3, 10))
            
            # Bedtime variations (21:30 - 23:30)
            bedtime_hour = np.random.randint(21, 24)
            bedtime_minute = np.random.choice([0, 15, 30, 45])
            bedtime = f"{bedtime_hour:02d}:{bedtime_minute:02d}"
            
            # Wake time based on sleep hours
            wake_hour = int((bedtime_hour + sleep_hours) % 24)
            if wake_hour < 5:
                wake_hour += 5
            wake_minute = np.random.choice([0, 15, 30, 45])
            wake_time = f"{wake_hour:02d}:{wake_minute:02d}"
            
            # Study hours (4-12 hours, with some variation)
            study_hours = np.clip(np.random.normal(8, 2), 3, 14)
            
            # Exercise (0-90 minutes, bimodal: either 0-15 or 30-60)
            exercise_minutes = int(
                np.random.choice([
                    np.random.randint(0, 20),
                    np.random.randint(30, 75)
                ])
            )
            
            # Meditation (0-45 minutes)
            meditation_minutes = int(np.random.choice([0, 10, 15, 20, 30]))
            
            # Diet quality (5-10, trending higher)
            diet_quality = int(np.clip(np.random.normal(7.5, 1.2), 4, 10))
            
            # Recall percentage (60-95%)
            recall_percent = int(np.clip(np.random.normal(78, 8), 55, 98))
            
            # PVT reaction time (200-450ms, lower is better)
            pvt_avg_ms = int(np.clip(np.random.normal(280, 50), 180, 500))
            
            # Mood, focus, energy (correlated with sleep quality)
            mood = int(np.clip(sleep_quality + np.random.randint(-2, 3), 3, 10))
            focus_score = int(np.clip(sleep_quality + np.random.randint(-1, 2), 4, 10))
            energy_level = int(np.clip(sleep_quality + np.random.randint(-2, 2), 3, 10))
            
            # Stress (inversely correlated with sleep)
            stress_level = int(np.clip(10 - sleep_quality + np.random.randint(-2, 3), 2, 10))
            
            # Water intake (1.5-4 liters)
            water_intake_liters = round(np.clip(np.random.normal(2.5, 0.6), 1.0, 4.5), 1)
            
            # Screen time (2-8 hours)
            screen_time_hours = round(np.clip(np.random.normal(4.5, 1.5), 2, 9), 1)
            
            # Random notes
            notes_options = [
                "Productive day, good focus",
                "Felt tired in afternoon",
                "Excellent study session",
                "Struggled with concentration",
                "Great workout today",
                "Need more sleep",
                "Very focused, minimal distractions",
                ""
            ]
            notes = np.random.choice(notes_options)
            
            # Calculate total index (simplified for mock data)
            total_index = int(
                (sleep_quality * 2) +
                (diet_quality * 2) +
                (recall_percent * 0.3) +
                (min(10, exercise_minutes / 4.5)) +
                (20 - (pvt_avg_ms - 200) / 15) -
                (abs(23 - int(bedtime.split(':')[0])))
            )
            total_index = max(50, min(95, total_index))  # Clamp to realistic range
            
            entry = {
                'date': current_date.strftime(DATE_FORMAT),
                'sleep_hours': round(sleep_hours, 1),
                'sleep_quality': sleep_quality,
                'bedtime': bedtime,
                'wake_time': wake_time,
                'study_hours': round(study_hours, 1),
                'exercise_minutes': exercise_minutes,
                'meditation_minutes': meditation_minutes,
                'diet_quality': diet_quality,
                'recall_percent': recall_percent,
                'pvt_avg_ms': pvt_avg_ms,
                'mood': mood,
                'focus_score': focus_score,
                'energy_level': energy_level,
                'stress_level': stress_level,
                'water_intake_liters': water_intake_liters,
                'screen_time_hours': screen_time_hours,
                'notes': notes,
                'total_index': total_index
            }
            
            mock_entries.append(entry)
        
        df = pd.DataFrame(mock_entries)
        return df
    
    def clear_data(self) -> bool:
        """
        Clear all data from the CSV file (use with caution).
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.data_file.exists():
                # Backup before clearing
                backup_path = self.data_file.with_suffix(
                    f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                )
                self.data_file.rename(backup_path)
                print(f"Data backed up to {backup_path}")
            
            # Create empty file
            empty_df = self.load_data()
            empty_df.to_csv(self.data_file, index=False)
            print("✅ Data cleared successfully")
            return True
        
        except Exception as e:
            print(f"❌ Error clearing data: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        Get summary statistics from stored data.
        
        Returns:
            Dictionary with key metrics (averages, trends, etc.)
        """
        df = self.load_data()
        
        if df.empty:
            return {
                'total_entries': 0,
                'date_range': 'No data',
                'avg_sleep': 0,
                'avg_study': 0,
                'avg_total_index': 0
            }
        
        stats = {
            'total_entries': len(df),
            'date_range': f"{df['date'].min()} to {df['date'].max()}",
            'avg_sleep': round(df['sleep_hours'].mean(), 1) if 'sleep_hours' in df else 0,
            'avg_study': round(df['study_hours'].mean(), 1) if 'study_hours' in df else 0,
            'avg_total_index': int(df['total_index'].mean()) if 'total_index' in df else 0,
            'best_day': df.loc[df['total_index'].idxmax(), 'date'] if 'total_index' in df and not df.empty else 'N/A',
            'best_score': int(df['total_index'].max()) if 'total_index' in df else 0
        }
        
        return stats


# Convenience functions
def quick_load() -> pd.DataFrame:
    """Quick wrapper to load data."""
    return DataManager().load_data()


def quick_save(entry: Dict) -> bool:
    """Quick wrapper to save entry."""
    return DataManager().save_entry(entry)


def quick_mock(days: int = 7) -> pd.DataFrame:
    """Quick wrapper to generate mock data."""
    return DataManager().get_mock_data(days)
