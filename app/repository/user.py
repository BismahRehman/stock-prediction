from fastapi import  HTTPException, status

from app.model.Blacklist_Table import BlacklistedToken
from app.model.user import User

from app.service.auth import verify_password, create_access_token ,hash_password
from sqlalchemy import select


async def loginuser(user,db):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if db_user.banned:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail="User is banned")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password for user",
        )
    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}




async def createuser(user,db):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar_one_or_none()
    if db_user:
        if db_user.banned:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="your account is temporary restricted")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")




    hashed_password = hash_password(user.password)

    new_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)



async def logout_user(credentials, db):
    token = credentials.credentials

    db_token = BlacklistedToken(token=token)
    db.add(db_token)
    await db.commit()

    return {"message": "Logged out successfully"}