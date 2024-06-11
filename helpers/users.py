import logging
import bcrypt


from models import Users, db


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed.decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_bytes)


def validate_user(username: str, password: str) -> Users:
    try:
        user = Users.query.filter_by(username=username).first()
        if user and check_password(password, user.password):
            return user
        else:
            return None

    except Exception as e:
        logging.error("Error validating user: %s", e)
        return None


def create_user(username: str, password: str) -> bool:
    try:
        user = Users(username=username, password=hash_password(password))
        db.session.add(user)
        db.session.commit()
        return True

    except Exception as e:
        logging.error("Error creating user: %s", e)
        return False


def get_user_by_id(user_id: int) -> Users:
    try:
        user = Users.query.get(user_id)
        return user

    except Exception as e:
        logging.error("Error getting user: %s", e)
        return None
