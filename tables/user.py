from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column
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