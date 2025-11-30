"""
UPSC Neuro-OS Scoring Engine
=============================
Pure Python domain logic for calculating cognitive performance scores.
Independent of UI framework - fully testable and reusable.

Author: Senior Python Software Architect
Date: November 29, 2025
"""

from datetime import datetime, time
from typing import Dict, Optional, Tuple
import math


class NeuroScorer:
    """
    Core scoring engine for UPSC Neuro-OS cognitive performance metrics.
    
    This class implements all scoring algorithms using evidence-based formulas
    for sleep quality, circadian rhythm, reaction time (PVT), and overall cognitive index.
    """
    
    # Scoring Constants
    OPTIMAL_SLEEP_HOURS = 7.5
    MAX_SLEEP_SCORE = 20
    MAX_PVT_SCORE = 20
    OPTIMAL_PVT_MS = 200  # Excellent reaction time
    PENALTY_PVT_MS = 500  # Baseline for penalties
    
    # Circadian Rhythm Constants
    OPTIMAL_BEDTIME_START = time(22, 0)  # 10:00 PM
    OPTIMAL_BEDTIME_END = time(23, 30)   # 11:30 PM
    OPTIMAL_WAKE_START = time(5, 30)     # 5:30 AM
    OPTIMAL_WAKE_END = time(7, 0)        # 7:00 AM
    
    def __init__(self):
        """Initialize the NeuroScorer with default configuration."""
        self.debug_mode = False
    
    def calculate_sleep_score(self, hours: float) -> float:
        """
        Calculate sleep score based on hours slept.
        
        Formula: min(MAX_SLEEP_SCORE, (hours / OPTIMAL_SLEEP_HOURS) * MAX_SLEEP_SCORE)
        
        Args:
            hours: Total sleep duration in hours (0.0 - 16.0)
        
        Returns:
            Sleep score (0.0 - 20.0)
        
        Raises:
            ValueError: If hours is negative or unrealistic (> 16)
        
        Examples:
            >>> scorer = NeuroScorer()
            >>> scorer.calculate_sleep_score(7.5)
            20.0
            >>> scorer.calculate_sleep_score(6.0)
            16.0
        """
        if hours < 0:
            raise ValueError("Sleep hours cannot be negative")
        if hours > 16:
            raise ValueError("Sleep hours cannot exceed 16 (unrealistic)")
        
        # Linear scaling with cap at optimal sleep
        raw_score = (hours / self.OPTIMAL_SLEEP_HOURS) * self.MAX_SLEEP_SCORE
        return min(self.MAX_SLEEP_SCORE, raw_score)
    
    def calculate_circadian_penalty(
        self, 
        bedtime: str, 
        wake_time: str
    ) -> int:
        """
        Calculate penalty based on circadian rhythm alignment.
        
        Penalties are applied for sleeping/waking outside optimal windows.
        Optimal: Sleep 10:00-11:30 PM, Wake 5:30-7:00 AM
        
        Args:
            bedtime: Bedtime in "HH:MM" format (24-hour)
            wake_time: Wake time in "HH:MM" format (24-hour)
        
        Returns:
            Penalty points (0-10, where 0 = perfect alignment)
        
        Examples:
            >>> scorer = NeuroScorer()
            >>> scorer.calculate_circadian_penalty("22:30", "06:00")
            0
            >>> scorer.calculate_circadian_penalty("02:00", "10:00")
            8
        """
        try:
            bed_dt = datetime.strptime(bedtime, "%H:%M").time()
            wake_dt = datetime.strptime(wake_time, "%H:%M").time()
        except ValueError:
            raise ValueError("Time must be in HH:MM format (24-hour)")
        
        penalty = 0
        
        # Bedtime penalty (1 point per hour deviation)
        if not (self.OPTIMAL_BEDTIME_START <= bed_dt <= self.OPTIMAL_BEDTIME_END):
            if bed_dt < self.OPTIMAL_BEDTIME_START:
                # Too early (before 10 PM)
                hours_diff = (
                    datetime.combine(datetime.today(), self.OPTIMAL_BEDTIME_START) -
                    datetime.combine(datetime.today(), bed_dt)
                ).total_seconds() / 3600
            else:
                # Too late (after 11:30 PM)
                hours_diff = (
                    datetime.combine(datetime.today(), bed_dt) -
                    datetime.combine(datetime.today(), self.OPTIMAL_BEDTIME_END)
                ).total_seconds() / 3600
            
            penalty += min(5, math.ceil(hours_diff))  # Max 5 points for bedtime
        
        # Wake time penalty (1 point per hour deviation)
        if not (self.OPTIMAL_WAKE_START <= wake_dt <= self.OPTIMAL_WAKE_END):
            if wake_dt < self.OPTIMAL_WAKE_START:
                # Too early (before 5:30 AM)
                hours_diff = (
                    datetime.combine(datetime.today(), self.OPTIMAL_WAKE_START) -
                    datetime.combine(datetime.today(), wake_dt)
                ).total_seconds() / 3600
            else:
                # Too late (after 7:00 AM)
                hours_diff = (
                    datetime.combine(datetime.today(), wake_dt) -
                    datetime.combine(datetime.today(), self.OPTIMAL_WAKE_END)
                ).total_seconds() / 3600
            
            penalty += min(5, math.ceil(hours_diff))  # Max 5 points for wake time
        
        return min(10, penalty)  # Cap at 10 total penalty points
    
    def calculate_pvt_score(self, ms: int) -> float:
        """
        Calculate Psychomotor Vigilance Task (PVT) score from reaction time.
        
        Formula: 
        - If ms <= 200: 20 points (excellent)
        - If ms > 500: max(0, 20 - (ms - 500) / 50)
        - Otherwise: Linear interpolation between 20 and penalty threshold
        
        Args:
            ms: Reaction time in milliseconds (100-3000)
        
        Returns:
            PVT score (0.0 - 20.0, higher is better)
        
        Raises:
            ValueError: If reaction time is unrealistic
        
        Examples:
            >>> scorer = NeuroScorer()
            >>> scorer.calculate_pvt_score(200)
            20.0
            >>> scorer.calculate_pvt_score(500)
            15.0
            >>> scorer.calculate_pvt_score(1000)
            10.0
        """
        if ms < 100:
            raise ValueError("Reaction time < 100ms is unrealistic (anticipation)")
        if ms > 3000:
            raise ValueError("Reaction time > 3000ms is unrealistic (lapse)")
        
        # Excellent performance: Full score
        if ms <= self.OPTIMAL_PVT_MS:
            return float(self.MAX_PVT_SCORE)
        
        # Good performance: Linear decay from optimal to penalty threshold
        if ms <= self.PENALTY_PVT_MS:
            score = self.MAX_PVT_SCORE - (
                (ms - self.OPTIMAL_PVT_MS) / 
                (self.PENALTY_PVT_MS - self.OPTIMAL_PVT_MS) * 5
            )
            return round(score, 2)
        
        # Poor performance: Penalty zone (500ms+)
        # Lose 1 point per 50ms above 500ms
        penalty = (ms - self.PENALTY_PVT_MS) / 50
        score = max(0.0, self.MAX_PVT_SCORE - 5 - penalty)
        
        return round(score, 2)
    
    def calculate_total_index(self, metrics: Dict[str, float]) -> int:
        """
        Calculate the Total Neuro-Performance Index from all metrics.
        
        Aggregates scores from multiple domains:
        - Sleep Score (20 points max)
        - PVT Score (20 points max)
        - Diet Score (20 points max, diet_quality * 2)
        - Recall Score (30 points max, recall_percent * 0.3)
        - Exercise Score (10 points max)
        - Circadian Penalty (deduction)
        
        Args:
            metrics: Dictionary containing:
                - sleep_score (float): Pre-calculated sleep score
                - pvt_score (float): Pre-calculated PVT score
                - diet_quality (int): 0-10 rating
                - recall_percent (int): 0-100 percentage
                - exercise_minutes (int): 0-120 minutes
                - circadian_penalty (int): 0-10 penalty points
        
        Returns:
            Total index (0-100 scale)
        
        Raises:
            KeyError: If required metrics are missing
            ValueError: If metric values are out of valid ranges
        
        Examples:
            >>> scorer = NeuroScorer()
            >>> metrics = {
            ...     'sleep_score': 20.0,
            ...     'pvt_score': 18.0,
            ...     'diet_quality': 8,
            ...     'recall_percent': 80,
            ...     'exercise_minutes': 45,
            ...     'circadian_penalty': 2
            ... }
            >>> scorer.calculate_total_index(metrics)
            86
        """
        # Validate required keys
        required_keys = {
            'sleep_score', 'pvt_score', 'diet_quality', 
            'recall_percent', 'exercise_minutes', 'circadian_penalty'
        }
        missing_keys = required_keys - set(metrics.keys())
        if missing_keys:
            raise KeyError(f"Missing required metrics: {missing_keys}")
        
        # Extract and validate metrics
        sleep_score = metrics['sleep_score']
        pvt_score = metrics['pvt_score']
        diet_quality = metrics['diet_quality']
        recall_percent = metrics['recall_percent']
        exercise_minutes = metrics['exercise_minutes']
        circadian_penalty = metrics['circadian_penalty']
        
        # Validation
        if not (0 <= sleep_score <= 20):
            raise ValueError(f"sleep_score must be 0-20, got {sleep_score}")
        if not (0 <= pvt_score <= 20):
            raise ValueError(f"pvt_score must be 0-20, got {pvt_score}")
        if not (0 <= diet_quality <= 10):
            raise ValueError(f"diet_quality must be 0-10, got {diet_quality}")
        if not (0 <= recall_percent <= 100):
            raise ValueError(f"recall_percent must be 0-100, got {recall_percent}")
        if not (0 <= exercise_minutes <= 120):
            raise ValueError(f"exercise_minutes must be 0-120, got {exercise_minutes}")
        if not (0 <= circadian_penalty <= 10):
            raise ValueError(f"circadian_penalty must be 0-10, got {circadian_penalty}")
        
        # Calculate component scores
        diet_score = diet_quality * 2  # Max 20 points
        recall_score = recall_percent * 0.3  # Max 30 points
        
        # Exercise score: Linear scaling (45 min = 10 points)
        exercise_score = min(10, (exercise_minutes / 45) * 10)
        
        # Total calculation
        total = (
            sleep_score +           # 20 points max
            pvt_score +             # 20 points max
            diet_score +            # 20 points max
            recall_score +          # 30 points max
            exercise_score -        # 10 points max
            circadian_penalty       # Deduction
        )
        
        # Ensure score is within 0-100 range
        total = max(0, min(100, total))
        
        return int(round(total))
    
    def get_performance_category(self, total_index: int) -> Tuple[str, str]:
        """
        Categorize performance based on total index score.
        
        Args:
            total_index: Total neuro-performance index (0-100)
        
        Returns:
            Tuple of (category, description)
        
        Examples:
            >>> scorer = NeuroScorer()
            >>> scorer.get_performance_category(92)
            ('Elite', 'Exceptional cognitive performance')
        """
        if total_index >= 90:
            return ("Elite", "Exceptional cognitive performance")
        elif total_index >= 80:
            return ("Excellent", "High cognitive efficiency")
        elif total_index >= 70:
            return ("Good", "Solid performance with room for improvement")
        elif total_index >= 60:
            return ("Fair", "Moderate performance - focus on key areas")
        elif total_index >= 50:
            return ("Below Average", "Significant improvement needed")
        else:
            return ("Poor", "Critical intervention required")


# Convenience functions for quick calculations
def quick_sleep_score(hours: float) -> float:
    """Quick wrapper for sleep score calculation."""
    return NeuroScorer().calculate_sleep_score(hours)


def quick_pvt_score(ms: int) -> float:
    """Quick wrapper for PVT score calculation."""
    return NeuroScorer().calculate_pvt_score(ms)


def quick_total_index(metrics: Dict[str, float]) -> int:
    """Quick wrapper for total index calculation."""
    return NeuroScorer().calculate_total_index(metrics)
