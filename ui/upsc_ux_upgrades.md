# 1. Automated Cycle Tracking (UX Upgrade)

Goal: Remove the manual `cycle_day` input to reduce friction. Implementation:
* New Persistence: Create a simple `user_config.json` to store static user settings.
* Sidebar Update: Add a collapsible section "⚙️ User Settings".
   * Input: `last_period_date` (Date Picker).
   * Save this date to `user_config.json`.
* Auto-Calculation Logic:
   * In the main daily form, automatically calculate `cycle_day`.
   * Formula: `days_diff = (current_date - last_period_date).days`
   * `current_cycle_day = (days_diff % 28) + 1`
   * Display the calculated day (e.g., "Cycle Day: 14 - Ovulation Phase") as a read-only info tag, and save it to the daily log CSV.

# 2. Time Series Data Fix (Critical)

Goal: Fix the broken X-Axis on charts where all data points appear at the same millisecond. Implementation:
* Modify the `utils/data_manager.py` mock data generator.
* Logic: When generating the 14 days of dummy data, use a loop to assign distinct, sequential dates (e.g., `today`, `today - 1`, `today - 2`...).
* Ensure the timestamp includes the Date (YYYY-MM-DD) so Plotly interprets it as a timeline, not a single point.

# 3. Solar Bonus Logic

Goal: Ensure Sunlight is rewarded. Implementation:
* In `utils/scoring.py`, ensure `calculate_sunlight_score(minutes)` is active.
* Logic: If `sunlight_minutes >= 15`: `+5 points`.
* Ensure this bonus is added to