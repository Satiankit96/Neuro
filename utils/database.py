"""
Database configuration and models for Neuro Index
"""

import os
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, Time, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base for declarative models
Base = declarative_base()

# Global variables for lazy initialization
_engine = None
_SessionLocal = None


def get_database_url():
    """
    Get database URL from environment.
    For Render/Hugging Face deployment, DATABASE_URL must be set as a secret.
    """
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        return None
    
    # Render uses postgres:// but SQLAlchemy needs postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    return database_url


def get_engine():
    """Get or create database engine (lazy initialization)."""
    global _engine
    
    if _engine is None:
        database_url = get_database_url()
        
        if not database_url:
            st.error("🚨 CRITICAL ERROR: DATABASE_URL not found!")
            st.warning("Please go to **Settings → Variables and secrets** and add a secret named `DATABASE_URL` with your PostgreSQL connection string.")
            st.info("You can get a free PostgreSQL database from Render.com or Neon.tech")
            st.stop()
        
        _engine = create_engine(database_url, echo=False)
    
    return _engine


def get_session_factory():
    """Get or create session factory (lazy initialization)."""
    global _SessionLocal
    
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine())
    
    return _SessionLocal


class DailyEntry(Base):
    """Model for daily productivity entries."""
    __tablename__ = 'daily_entries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    
    # Input metrics
    study_hours = Column(Float, nullable=False)
    screen_time_minutes = Column(Integer, nullable=False)
    recall_percent = Column(Float, nullable=False)
    sleep_hours = Column(Float, nullable=False)
    bedtime = Column(Time, nullable=False)
    wake_time = Column(Time, nullable=False)
    diet_quality = Column(Integer, nullable=False)
    exercise_minutes = Column(Integer, nullable=False)
    sunlight_minutes = Column(Integer, default=0)
    cycle_day = Column(Integer, nullable=False)
    
    # Calculated scores
    study_score = Column(Float, nullable=False)
    recall_score = Column(Float, nullable=False)
    sleep_score = Column(Float, nullable=False)
    diet_score = Column(Float, nullable=False)
    exercise_score = Column(Float, nullable=False)
    sunlight_score = Column(Float, default=0)
    circadian_penalty = Column(Float, default=0)
    distraction_penalty = Column(Float, default=0)
    total_index = Column(Float, nullable=False)
    cognitive_roi = Column(Float, nullable=False)
    
    def to_dict(self):
        """Convert entry to dictionary."""
        return {
            'id': self.id,
            'date': self.date,
            'study_hours': self.study_hours,
            'screen_time_minutes': self.screen_time_minutes,
            'recall_percent': self.recall_percent,
            'sleep_hours': self.sleep_hours,
            'bedtime': self.bedtime,
            'wake_time': self.wake_time,
            'diet_quality': self.diet_quality,
            'exercise_minutes': self.exercise_minutes,
            'sunlight_minutes': self.sunlight_minutes,
            'cycle_day': self.cycle_day,
            'study_score': self.study_score,
            'recall_score': self.recall_score,
            'sleep_score': self.sleep_score,
            'diet_score': self.diet_score,
            'exercise_score': self.exercise_score,
            'sunlight_score': self.sunlight_score,
            'circadian_penalty': self.circadian_penalty,
            'distraction_penalty': self.distraction_penalty,
            'total_index': self.total_index,
            'cognitive_roi': self.cognitive_roi
        }


class UserConfig(Base):
    """Model for user configuration settings."""
    __tablename__ = 'user_config'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(String(500), nullable=True)
    
    def to_dict(self):
        """Convert config to dictionary."""
        return {
            'key': self.key,
            'value': self.value
        }


def init_database():
    """Initialize database tables. Call this once after deployment."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def get_session():
    """Get a new database session."""
    SessionLocal = get_session_factory()
    return SessionLocal()
