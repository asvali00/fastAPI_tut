from passlib.context import CryptContext

# defining hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashing(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    # nemoj da te buni ova verify metoda, to dolazi od CryptContext-a ne od funkcije koju su liniju prije definira
    return pwd_context.verify(plain_password, hashed_password)
