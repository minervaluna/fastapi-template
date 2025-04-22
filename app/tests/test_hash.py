from app.core.security import get_password_hash, verify_password

# password_hash = get_password_hash('123456')
# print(f"password_hash: {password_hash}")
password_hash = '$2b$12$ilnIbLjIHwNT26MHm9b4UOt6MCtVhDQvq8T3vhu8SsDtt8LdP0sk6'
eq = verify_password('123456', password_hash)
print(f"eq: {eq}")
