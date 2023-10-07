from src.database.models import DatabaseUser

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
    }
}


def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return DatabaseUser(**user_dict)
