import models
from sqlalchemy.orm import Session
import bcrypt
import schemas
import psycopg2

conn = psycopg2.connect(host="docker.for.mac.localhost",
                        database="staging",
                        user="postgres",
                        password="lobb123")
cur = conn.cursor()


def get_user_by_username(username: str):
    cur.execute(f"select * from public.user_info where username = '{username}'")
    return cur.fetchone()


def create_user(user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf8')
    print("Hashed password:", hashed_password)
    db_user = schemas.UserCreate(username=user.username, password=hashed_password, fullname=user.fullname)
    cur.execute(
        "Insert into public.user_info (username,password,fullname) values (%s,%s,%s)",
        (user.username, hashed_password, user.fullname))
    conn.commit()
    cur.close()
    conn.close()
    return db_user


# def create_user():
#     cur.execute(
#         "Insert into public.user_info (id,username,password,fullname) values (2,'test1','testfull','testpassword')")
#     conn.commit()
#     cur.close()
#     conn.close()
