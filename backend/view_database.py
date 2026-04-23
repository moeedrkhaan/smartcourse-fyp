"""
View SmartCourse Database Contents
Quick script to view all data in SQLite database
"""

import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = 'smartcourse.db'

def view_database():
    """Display all database contents"""
    
    try:
        conn = sqlite3.connect(DB_PATH)
        
        print("=" * 70)
        print("SMARTCOURSE DATABASE VIEWER")
        print("=" * 70)
        print(f"Database: {DB_PATH}")
        print(f"Accessed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Users
        print("\n👤 USERS")
        print("-" * 70)
        df_users = pd.read_sql_query(
            "SELECT id, email, username, created_at FROM users ORDER BY created_at DESC",
            conn
        )
        if len(df_users) > 0:
            print(f"Total users: {len(df_users)}")
            print("\nRegistered users:")
            print(df_users.to_string(index=False))
        else:
            print("No users registered yet.")
        
        # Search History
        print("\n\n📊 SEARCH HISTORY")
        print("-" * 70)
        df_history = pd.read_sql_query(
            "SELECT id, user_id, query, model, results_count, timestamp FROM search_history ORDER BY timestamp DESC LIMIT 20",
            conn
        )
        if len(df_history) > 0:
            print(f"Total searches: {len(df_history)}")
            print("\nRecent searches:")
            print(df_history.to_string(index=False))
        else:
            print("No search history yet.")
        
        # Saved Recommendations
        print("\n\n💾 SAVED RECOMMENDATIONS")
        print("-" * 70)
        df_saved = pd.read_sql_query(
            "SELECT id, user_id, course_title, course_provider, query, model, relevance_score, timestamp FROM saved_recommendations ORDER BY timestamp DESC LIMIT 20",
            conn
        )
        if len(df_saved) > 0:
            print(f"Total saved: {len(df_saved)}")
            print("\nRecent saves:")
            print(df_saved.to_string(index=False))
        else:
            print("No saved recommendations yet.")
        
        # Statistics
        print("\n\n📈 STATISTICS")
        print("-" * 70)
        
        # Count by model
        model_counts = pd.read_sql_query(
            """
            SELECT model, COUNT(*) as count 
            FROM search_history 
            GROUP BY model
            """,
            conn
        )
        if len(model_counts) > 0:
            print("\nSearches by model:")
            print(model_counts.to_string(index=False))
        
        # Most searched queries
        top_queries = pd.read_sql_query(
            """
            SELECT query, COUNT(*) as search_count 
            FROM search_history 
            GROUP BY query 
            ORDER BY search_count DESC 
            LIMIT 5
            """,
            conn
        )
        if len(top_queries) > 0:
            print("\nTop 5 queries:")
            print(top_queries.to_string(index=False))
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✓ Database viewed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def export_to_csv():
    """Export database tables to CSV files"""
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Export search history
        df_history = pd.read_sql_query("SELECT * FROM search_history", conn)
        df_history.to_csv('search_history.csv', index=False)
        print(f"✓ Exported {len(df_history)} records to search_history.csv")
        
        # Export saved recommendations
        df_saved = pd.read_sql_query("SELECT * FROM saved_recommendations", conn)
        df_saved.to_csv('saved_recommendations.csv', index=False)
        print(f"✓ Exported {len(df_saved)} records to saved_recommendations.csv")
        
        conn.close()
        print("\n✓ Export completed!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def clear_database():
    """Clear all data from database (use with caution!)"""
    confirm = input("\n⚠️  Are you sure you want to DELETE ALL DATA? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM search_history")
            cursor.execute("DELETE FROM saved_recommendations")
            
            conn.commit()
            conn.close()
            
            print("✓ Database cleared successfully!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    else:
        print("Cancelled.")

if __name__ == "__main__":
    print("\nSmartCourse Database Tools")
    print("1. View Database")
    print("2. Export to CSV")
    print("3. Clear Database (DANGER!)")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ")
    
    if choice == '1':
        view_database()
    elif choice == '2':
        export_to_csv()
    elif choice == '3':
        clear_database()
    else:
        print("Exiting...")
