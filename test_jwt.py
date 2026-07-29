from app.utils.jwt_handler import create_access_token, verify_access_token

token = create_access_token(
    {"user_id": 1, "email": "pushpak@example.com"}
)

print("JWT Token:\n")
print(token)

print("\nDecoded Payload:\n")
print(verify_access_token(token))