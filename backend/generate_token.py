from datetime import timedelta
from auth import create_access_token

# Use your actual user_id
user_id = "b3deda24-1e74-492b-b2b5-9e5ffed10377"

# Create token
access_token = create_access_token(
    data={"sub": user_id},
    expires_delta=timedelta(minutes=30)  # Token valid for 30 minutes
)

print("Your JWT token:\n")
print(access_token)
