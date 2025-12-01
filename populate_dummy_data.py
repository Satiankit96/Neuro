"""
Populate UPSC Neuro-OS with 4 months of dummy data
Run this script to generate realistic test data.
"""

from utils.data_manager import DataManager

def main():
    print("🎲 Generating dummy data for UPSC Neuro-OS...")
    print("=" * 60)
    
    # Initialize data manager
    data_manager = DataManager("upsc_logs.csv")
    
    # Generate 120 days (4 months) of dummy data
    data_manager.generate_dummy_data(days=120)
    
    print("=" * 60)
    print("✅ Done! You can now view the data in the app.")
    print("📊 Navigate to http://localhost:8508 and check the Dashboard page.")

if __name__ == "__main__":
    main()
