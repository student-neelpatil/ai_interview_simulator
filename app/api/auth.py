from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)


from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.user import User

from app.schemas.auth_schema import (
    SignUp,
    Login
)

from app.core.security import (
    hashing_password,
    verify_password,
    create_access_token
)

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

#signup api

@router.post("/signup")
def signup(
    user_data:SignUp,
    db:Session=Depends(get_db)
):
    existing_user=db.query(User).filter(
        User.email==user_data.email
    ).first()

    if existing_user :
        raise HTTPException(
            status_code=400,
            detail="email already registered"
        )
    
    hashedpassword=hashing_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashedpassword
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }


#login api

@router.post("/login")
def login ( user_data:Login,db: Session = Depends(get_db)):
 

    #checking if user exist or not 

    existing_user = db.query(User).filter(
        User.email==user_data.email
    ).first()
    
    if not existing_user:
        raise HTTPException(
            status_code=400,
            detail="user not found or invalid credentils"
        )
    
    #hash lastest password

    

    is_password_valid = verify_password(user_data.password, str(existing_user.password_hash))

    if not is_password_valid:
        raise HTTPException(
            status_code=400,
            detail="invalid credential"
        )
    
    token=create_access_token({
         "sub": existing_user.email
    })

   
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }
