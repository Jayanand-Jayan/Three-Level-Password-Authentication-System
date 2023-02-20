from sqlalchemy.orm import Session
import models, schemas
import bcrypt 

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(username=user.username, hashed_password=hashed_password, phno=user.phno)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user