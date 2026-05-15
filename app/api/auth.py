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
        password=hashedpassword
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }