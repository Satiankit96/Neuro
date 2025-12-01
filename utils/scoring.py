"""
Productivity-First Scoring Engine for UPSC Neuro-OS
Implements a simple, transparent scoring system focused on study productivity.
"""

from datetime import time


def calculate_study_score(hours: float) -> float:
    """
    Study Score: 30 points maximum.
    Linear scaling to 8 hours.
    
    Args:
        hours: Study hours (float)
    
    Returns:
        Score from 0-30 points
    """
    if hours <= 0:
        return 0.0
    if hours >= 8:
        return 30.0
    return (hours / 8) * 30


def calculate_recall_score(percent: float) -> float:
    """
    Recall Score: 20 points maximum.
    Direct conversion: percent * 0.2
    
    Args:
        percent: Recall percentage (0-100)
    
    Returns:
        Score from 0-20 points
    """
    if percent <= 0:
        return 0.0
    if percent >= 100:
        return 20.0
    return percent * 0.2


def calculate_sleep_score(hours: float) -> float:
    """
    Sleep Score: 20 points maximum.
    -2 points per hour deviation from 7.5 hours.
    
    Args:
        hours: Sleep hours (float)
    
    Returns:
        Score from 0-20 points
    """
    optimal_sleep = 7.5
    deviation = abs(hours - optimal_sleep)
    score = 20 - (deviation * 2)
    return max(0.0, min(20.0, score))


def calculate_diet_score(quality: float) -> float:
    """
    Diet Score: 20 points maximum.
    Direct conversion: quality * 2
    
    Args:
        quality: Diet quality rating (0-10)
    
    Returns:
        Score from 0-20 points
    """
    if quality <= 0:
        return 0.0
    if quality >= 10:
        return 20.0
    return quality * 2


def calculate_exercise_score(minutes: int) -> float:
    """
    Exercise Score: 10 points maximum.
    Linear scaling to 30 minutes.
    
    Args:
        minutes: Exercise minutes (int)
    
    Returns:
        Score from 0-10 points
    """
    if minutes <= 0:
        return 0.0
    if minutes >= 30:
        return 10.0
    return (minutes / 30) * 10


def calculate_sunlight_score(minutes: int) -> float:
    """
    Sunlight Bonus Score: 5 points maximum.
    Bonus awarded if sunlight >= 15 minutes.
    
    Args:
        minutes: Sunlight exposure minutes (int)
    
    Returns:
        Score: 5 if >= 15 mins, else 0
    """
    if minutes >= 15:
        return 5.0
    return 0.0


def calculate_circadian_penalty(bedtime: time, wake_time: time) -> float:
    """
    Circadian Penalty: Maximum -10 points.
    - Bedtime > 22:30: -3 points
    - Bedtime > 23:30: -5 points
    - Wake time > 06:30: -2 points
    
    Args:
        bedtime: Bedtime as time object
        wake_time: Wake time as time object
    
    Returns:
        Penalty from 0 to -10 points
    """
    penalty = 0.0
    
    # Bedtime penalties
    if bedtime > time(23, 30):
        penalty -= 5.0
    elif bedtime > time(22, 30):
        penalty -= 3.0
    
    # Wake time penalty
    if wake_time > time(6, 30):
        penalty -= 2.0
    
    # Cap at -10
    return max(-10.0, penalty)


def calculate_distraction_penalty(screen_time_minutes: int) -> float:
    """
    Distraction Penalty: Maximum -10 points.
    -2 points for every 30 minutes screen time > 60 minutes.
    
    Args:
        screen_time_minutes: Screen time in minutes
    
    Returns:
        Penalty from 0 to -10 points
    """
    if screen_time_minutes <= 60:
        return 0.0
    
    excess_minutes = screen_time_minutes - 60
    penalty_blocks = excess_minutes // 30
    penalty = penalty_blocks * -2.0
    
    # Cap at -10
    return max(-10.0, penalty)


def calculate_total_index(
    study_hours: float,
    recall_percent: float,
    sleep_hours: float,
    diet_quality: float,
    exercise_minutes: int,
    bedtime: time,
    wake_time: time,
    screen_time_minutes: int,
    sunlight_minutes: int = 0
) -> dict:
    """
    Calculate the Total Productivity Index.
    
    Returns:
        Dictionary with component scores and total index (0-100)
    """
    # Calculate component scores
    study_score = calculate_study_score(study_hours)
    recall_score = calculate_recall_score(recall_percent)
    sleep_score = calculate_sleep_score(sleep_hours)
    diet_score = calculate_diet_score(diet_quality)
    exercise_score = calculate_exercise_score(exercise_minutes)
    sunlight_score = calculate_sunlight_score(sunlight_minutes)
    
    # Calculate penalties
    circadian_penalty = calculate_circadian_penalty(bedtime, wake_time)
    distraction_penalty = calculate_distraction_penalty(screen_time_minutes)
    
    # Calculate total (clamp 0-100)
    total = (
        study_score + 
        recall_score + 
        sleep_score + 
        diet_score + 
        exercise_score + 
        sunlight_score +
        circadian_penalty + 
        distraction_penalty
    )
    total = max(0.0, min(100.0, total))
    
    return {
        'study_score': round(study_score, 2),
        'recall_score': round(recall_score, 2),
        'sleep_score': round(sleep_score, 2),
        'diet_score': round(diet_score, 2),
        'exercise_score': round(exercise_score, 2),
        'sunlight_score': round(sunlight_score, 2),
        'circadian_penalty': round(circadian_penalty, 2),
        'distraction_penalty': round(distraction_penalty, 2),
        'total_index': round(total, 2)
    }


def calculate_cognitive_roi(recall_percent: float, study_hours: float) -> float:
    """
    Cognitive ROI: Measures retention per hour of work.
    Formula: recall_percent / study_hours
    
    Args:
        recall_percent: Recall percentage (0-100)
        study_hours: Study hours (float)
    
    Returns:
        ROI value (retention per hour)
    """
    if study_hours <= 0:
        return 0.0
    return recall_percent / study_hours
