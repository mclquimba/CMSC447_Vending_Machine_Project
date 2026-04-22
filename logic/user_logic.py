from sqlalchemy import select
from sqlalchemy.orm import Session

from tables.user import User, Role
from utilities.error_checking import ErrorChecking as ec

def get_username(session: Session, username: str) -> bool:
    query = select(User.username).where(User.username == username)
    if session.scalars(query).first() is None:
        return False
    return True

def get_next_id(session: Session) -> int:
    query = select(User.user_id).order_by(User.user_id)
    ids = session.scalars(query).all()
    
    counter = 1
    for id in ids:
        if counter != id:
            return counter
        counter += 1
        
    return counter

def get_admin(session: Session) -> bool:
    query = select(User.role).where(User.role == Role.ADMIN)
    if session.scalars(query).first() is None:
        return False
    return True

def add_user(session: Session, username: str, role: Role) -> User:
    errors = {}
    errors_username = []
    errors_role = []
    
    ec.check_username_nop(username, errors_username)
    
    for field, field_errors in (("username", errors_username)):
        if field_errors:
            errors[field] = field_errors
            
    if errors:
        raise ValueError(errors)
    
    # check if username is in the database already, if it is return error
    if get_username(session, username):
        errors_username.append("Username taken.")
        errors["username"] = errors_username
        raise ValueError(errors)
    
    # check if role is admin, if so then check if admin already exists, if so then return error
    if role == Role.ADMIN:
        if get_admin(session):
            errors_role.append("Can not have multiple Administrator roles.")
            errors["role"] = errors_role
            raise ValueError(errors)
    
    u_id = get_next_id(session)
    u_name = username
    u_role = role
    
    new_user = User(user_id=u_id, username=u_name, role=u_role)
    
    session.add(new_user)
    session.flush()
    
    return new_user
    
"""
 def modify_user(session: Session, user_id: str, username: str, role: Role) -> User:
    errors = {}
    errors_user_id = []
    errors_username = []
    errors_role = []
"""
    
def delete_user(session: Session, user_id: str) -> dict:
    errors = {}
    errors_user_id = []
    
    user_id_stripped = user_id.strip()
    
    ec.check_user_id_nop(user_id_stripped, errors_user_id)
    
    for field, field_errors in (("user_id", errors_user_id)):
        if field_errors:
            errors[field] = field_errors
            
    if errors:
        raise ValueError(errors)
    
    int_user_id = int(user_id_stripped)
    
    query = select(User).where(User.user_id == int_user_id)
    user = session.scalars(query).first()
    if user is None:
        errors_user_id.append(f"User {int_user_id} does not exist.")
        errors["user_id"] = errors_user_id
        raise ValueError(errors)
    
    user_info = {
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role
    }
    
    session.delete(user)
    session.flush()
    
    return user_info