import requests
import os
from database import SessionLocal
from models import User
import uuid

# 1️⃣ Supabase API details
SUPABASE_URL = "https://<YOUR_PROJECT_ID>.supabase.co"
SUPABASE_KEY = "<YOUR_SUPABASE_SERVICE_ROLE_KEY>"  # Service role key for admin-level access

# 2️⃣ Get list of users from Supabase
response = requests.get(
    f"{SUPABASE_URL}/auth/v1/admin/users",
    headers={
        "apiKey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    },
)
response.raise_for_status()
users = response.json()["users"]

# 3️⃣ Connect to local DB
db = SessionLocal()

for user in users:
    user_id = user["id"]
    email = user["email"]

    # Check if user exists in local DB
    existing = db.query(User).filter(User.id == user_id).first()
    if existing:
        print(f"User {email} already exists. Skipping.")
        continue

    # Create local user
    new_user = User(
        id=uuid.UUID(user_id),
        username=email.split("@")[0],  # Default username
        email=email,
        hashed_password="",             # Supabase manages password
    )
    db.add(new_user)
    print(f"Added {email} to local DB.")

db.commit()
db.close()
print("Sync complete.")
