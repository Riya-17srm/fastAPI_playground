from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import model, schemas, utils
from auth_database import get_db
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm


SECRET_KEY= "Xhm8ioaCGqQoNx3MJgGDl5FR6IUKyOEizq4kBd9_IPk"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES= 30

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({'exp':expire})
    encode_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

app=FastAPI() 

@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session= Depends(get_db)):
    existing_user=db.query(model.User).filter(model.User.username==user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists")
    
    hashed_password=utils.hash_password(user.password)

    new_user=model.User(
        username=user.username,
        email=user.email,
        hashed_password= hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'id':new_user.id, 'username': new_user.username, 'email':new_user.email, 'role':new_user.role}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=db.query(model.User).filter(model.User.username==form_data.username).first()
    if not user:
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username")
    
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Password')
    
    token_data={'sub': user.username, 'role':user.role}
    token=create_access_token(token_data)
    return {"access_token": token, "token_type":"bearer"}


