from app.schemas import User, UserCreate, UserUpdate
from app.utils import verify_password, get_password_hash
from typing import List

fake_users_db: dict[int, User] = {}
fake_passwords: dict[int, str] = {}
counter = 1


def create_user(user: UserCreate) -> User:
    global counter
    hashed_pw = get_password_hash(user.password)
    new_user = User(id=counter, name=user.name, email=user.email)
    fake_users_db[counter] = new_user
    fake_passwords[counter] = hashed_pw
    counter += 1
    return new_user


def get_user(user_id: int) -> User:
    return fake_users_db.get(user_id)


def get_user_by_email(email: str):
    print(f"user emails : {fake_users_db.items()}")
    for uid, u in fake_users_db.items():
        if u.email == email:
            return User(id=u.id, name=u.name, email=u.email, password=u.password)
    return None


def get_user_by_name(email: str):
    print(f"user emails : {fake_users_db.items()}")
    for uid, u in fake_users_db.items():
        if u.name == email:
            return User(id=u.id, name=u.name, email=u.email, password=u.password)
    return None


def list_users(q: str = None) -> List[User]:
    if q:
        return [u for u in fake_users_db.values() if q.lower() in u.name.lower()]
    return list(fake_users_db.values())


def update_user(user_id: int, user: UserUpdate):
    if user_id not in fake_users_db:
        return None
    stored = fake_users_db[user_id]
    updated = stored.copy(update=user.dict(exclude_unset=True))
    fake_users_db[user_id] = updated
    return updated


def delete_user(user_id: int):
    return fake_users_db.pop(user_id, None)


def generate_fake_users():
    fake_users_db[1] = User(id=1, name="sabbu", email="sabbu@wells.com", password=get_password_hash("sabbu"))
    fake_users_db[2] = User(id=2, name="padma", email="padma@wells.com", password=get_password_hash("padma"))
    fake_users_db[3] = User(id=3, name="chandra", email="chandra@wells.com", password=get_password_hash("chandra"))
