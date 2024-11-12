from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def authenticate_user(userInDB, session, username: str, password: str):
    user = session.query(userInDB).filter(userInDB.email == username).first()
    # user = session.exec(select(userInDB).where(userInDB.email == username)).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

