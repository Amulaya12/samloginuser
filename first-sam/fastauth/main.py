from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, auth
from database import DBInit
from mangum import Mangum
import psycopg2

# These constants go in a specific config file
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
handle = Mangum(app)


@app.post("/users/register", status_code=201, response_model=schemas.UserCreate, tags=["users"])
def register_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="Username already registered")
    return crud.create_user(user=user)


@app.post("/users/auth", response_model=schemas.Token, tags=["users"])
def authenticate_user(user: schemas.UserAuthenticate):
    # import pdb;
    # pdb.set_trace()
    db_user = crud.get_user_by_username(username=user.username)
    if db_user is None:
        raise HTTPException(status_code=403, detail="Username doesn't exit")
    else:
        is_password_correct = auth.check_username_password(user)
        print("Password correct:", is_password_correct)
        if is_password_correct is False:
            raise HTTPException(status_code=403, detail="Username or password is incorrect")
        else:
            from datetime import timedelta
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = auth.encode_jwt_token(
                data={"sub": user.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "Bearer"}
