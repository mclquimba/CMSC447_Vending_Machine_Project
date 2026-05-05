from sqlalchemy import Enum, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
import enum

MAX_USERNAME_CHARS = 500

from tables import Base

class Role(enum.Enum):
    ADMIN = "Administrator"
    STAFF = "Staff"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(MAX_USERNAME_CHARS), nullable=False, unique=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    
    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username}, role={self.role})"

    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return (
            f"User(user_id={self.user_id}, "
            f"username={self.username}, "
            f"role={self.role}, "
            f"last_login={self.last_login})"
        )