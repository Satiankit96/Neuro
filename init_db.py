"""
Database Initialization Script for Neuro Index
Run this locally to set up PostgreSQL database and populate with dummy data.
"""

from utils.database import init_database
from utils.db_data_manager import DataManager
import sys

def main():
    print("🔧 Initializing Neuro Index Database...")
    
    try:
        # Create tables
        init_database()
        
        # Generate dummy data
        print("\n📊 Generating dummy data...")
        data_manager = DataManager()
        data_manager.generate_dummy_data(days=120)
        
        print("\n✅ Database setup complete!")
        print("✅ Added 120 days of dummy data")
        print("\nNext steps:")
        print("1. Run app: streamlit run app.py --server.port 8508")
        print("2. Toggle to Dashboard tab to see visualizations")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        print("\nTroubleshooting:")
        print("1. Check PostgreSQL is running")
        print("2. Verify database 'neuro_index' exists")
        print("3. Check connection: postgresql://postgres:postgres@localhost:5432/neuro_index")
        sys.exit(1)
    print("🚀 You can now run the Streamlit app")

if __name__ == "__main__":
    main()
