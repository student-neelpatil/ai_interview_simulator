import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()

#hashing the password
def hashing_password(password:str):

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode("utf-8"),salt)

    return hashed_password.decode("utf-8")


#verifying the password
def verify_password(plain_password:str,hashed_password:str):
    
    return bcrypt.checkpw(plain_password.encode(),hashed_password.encode())
    

#creating access token

def create_access_token(data:dict):

    encoded_data=data.copy()
     
     #expire time of token
    expire_time=datetime.utcnow() + timedelta(minutes=30)

    #adding expire time in encoded_data dict

    encoded_data.update({
        "exp":expire_time
    })

    token = jwt.encode(
        encoded_data,
        os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM")
    )

    return token




#example of encoded_data
#{
 # "sub": "neel@example.com",
 # "exp": 123456789
#}

def decode_access_token(token: str):

    payload = jwt.decode(
        token,
        os.getenv("SECRET_KEY"),
        algorithms=os.getenv("ALGORITHM")
    )

    return payload