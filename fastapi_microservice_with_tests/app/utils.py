from passlib.context import CryptContext

# Initialize CryptContext with bcrypt as the hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to verify if the password matches the hash
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to generate a password hash
def get_password_hash(password):
    return pwd_context.hash(password)
