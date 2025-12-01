# UPSC Neuro-OS: Metrics Calculation Logic

## 📍 File Location
**Primary Logic**: `utils/scoring.py`  
**Usage**: Called in `app.py` (line ~165) when saving entry

---

## 🎯 Core Metrics (Total Index: 0-100)

### **Study Score** (Max: 30 points)
```python
# Linear scaling to 8 hours
score = (study_hours / 8) * 30
# File: utils/scoring.py, Line 9-23
```
- 8+ hours → 30 points
- 4 hours → 15 points
- 0 hours → 0 points

---

### **Recall Score** (Max: 20 points)
```python
# Direct conversion
score = recall_percent * 0.2
# File: utils/scoring.py, Line 27-42
```
- 100% recall → 20 points
- 50% recall → 10 points

---

### **Sleep Score** (Max: 20 points)
```python
# Optimal: 7.5 hours, -2 points per hour deviation
deviation = abs(sleep_hours - 7.5)
score = 20 - (deviation * 2)
# File: utils/scoring.py, Line 45-59
```
- 7.5 hours → 20 points
- 6.5 or 8.5 hours → 18 points
- 5.5 or 9.5 hours → 16 points

---

### **Diet Score** (Max: 20 points)
```python
# Direct conversion from 1-10 scale
score = diet_quality * 2
# File: utils/scoring.py, Line 62-77
```
- Quality 10/10 → 20 points
- Quality 5/10 → 10 points

---

### **Exercise Score** (Max: 10 points)
```python
# Linear scaling to 30 minutes
score = (exercise_minutes / 30) * 10
# File: utils/scoring.py, Line 80-95
```
- 30+ minutes → 10 points
- 15 minutes → 5 points

---

### **Sunlight Bonus** (Max: 5 points)
```python
# Binary threshold at 15 minutes
score = 5 if sunlight_minutes >= 15 else 0
# File: utils/scoring.py, Line 98-111
```
- ≥15 minutes → 5 points
- <15 minutes → 0 points

---

## ⚠️ Penalties (Max: -20 points)

### **Circadian Penalty** (Max: -10)
```python
# Bedtime penalties
if bedtime > 23:30 → -5 points
elif bedtime > 22:30 → -3 points

# Wake time penalty
if wake_time > 06:30 → -2 points
# File: utils/scoring.py, Line 114-141
```

---

### **Distraction Penalty** (Max: -10)
```python
# -2 points per 30 min block over 60 min
if screen_time > 60:
    excess = screen_time - 60
    penalty = (excess // 30) * -2
# File: utils/scoring.py, Line 144-165
```
- 60 min → 0 penalty
- 90 min → -2 points
- 120 min → -4 points
- 150+ min → -6 points

---

## 🧠 Calculated Metrics

### **Cognitive ROI**
```python
# Retention efficiency per hour
cognitive_roi = recall_percent / study_hours
# File: utils/scoring.py, Line 221-236
# Used in: app.py Line 162
```
**Example**: 80% recall ÷ 4 hours = **20.0 ROI**

---

### **Cycle Day** (Auto-calculated)
```python
# Days since last period start
cycle_day = (today - last_period_date).days + 1
# File: utils/data_manager.py, Line 262
# Used in: app.py Line 90
```
**Range**: 1-28 days (auto-wrapping)

---

## 📊 Final Total Index
```python
total = study + recall + sleep + diet + exercise + sunlight 
        + circadian_penalty + distraction_penalty
total = clamp(total, 0, 100)  # Never below 0 or above 100
# File: utils/scoring.py, Line 203-211
```
