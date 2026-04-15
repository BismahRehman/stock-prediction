from fastapi import HTTPException, status
from sqlalchemy import select

from app.model.Blacklist_Table import BlacklistedToken
from app.model.user import User
from app.service.auth import verify_password, create_access_token, hash_password


# -----------------------------------
# LOGIN USER (Authentication flow)
# -----------------------------------
async def loginuser(user, db):

    # Fetch user by email
    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    db_user = result.scalar_one_or_none()

    # Validate existence
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )

    # Check if user is banned
    if db_user.banned:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is banned"
        )

    # Verify password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password for user"
        )

    # Generate JWT token
    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}


# -----------------------------------
# CREATE USER (Registration flow)
# -----------------------------------
async def createuser(user, db):

    # Check if user exists
    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    db_user = result.scalar_one_or_none()

    # If exists → handle states
    if db_user:
        if db_user.banned:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="your account is temporary restricted"
            )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password before storing
    hashed_password = hash_password(user.password)

    # Create user object
    new_user = User(
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)


# -----------------------------------
# LOGOUT USER (Token blacklisting)
# -----------------------------------
async def logout_user(credentials, db):

    # Extract JWT token from request
    token = credentials.credentials

    # Store token in blacklist table
    db_token = BlacklistedToken(token=token)

    db.add(db_token)
    await db.commit()

    return {"message": "Logged out successfully"}