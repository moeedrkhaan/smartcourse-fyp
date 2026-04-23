"""
Quick script to check users in database
"""
import sqlite3

conn = sqlite3.connect('smartcourse.db')
cursor = conn.cursor()

print("\n" + "="*70)
print("👤 REGISTERED USERS")
print("="*70)

cursor.execute("SELECT id, email, username, created_at FROM users ORDER BY id")
users = cursor.fetchall()

if users:
    print(f"\nTotal users: {len(users)}\n")
    for user in users:
        print(f"ID: {user[0]}")
        print(f"Email: {user[1]}")
        print(f"Username: {user[2]}")
        print(f"Created: {user[3]}")
        print("-" * 70)
else:
    print("\nNo users registered yet.")
    print("-" * 70)

# Check search history count per user
print("\n📊 SEARCH HISTORY BY USER")
print("="*70)
cursor.execute("""
    SELECT user_id, COUNT(*) as searches 
    FROM search_history 
    GROUP BY user_id
""")
history = cursor.fetchall()
if history:
    for row in history:
        user_id = row[0] if row[0] else "Guest"
        print(f"User ID {user_id}: {row[1]} searches")
else:
    print("No search history yet.")

# Check saved items per user
print("\n💾 SAVED ITEMS BY USER")
print("="*70)
cursor.execute("""
    SELECT user_id, COUNT(*) as saved 
    FROM saved_recommendations 
    GROUP BY user_id
""")
saved = cursor.fetchall()
if saved:
    for row in saved:
        user_id = row[0] if row[0] else "Guest"
        print(f"User ID {user_id}: {row[1]} saved courses")
else:
    print("No saved items yet.")

conn.close()
print("\n" + "="*70 + "\n")
