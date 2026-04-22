from sqlalchemy import ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from datetime import datetime
from pytz import timezone

from tables import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    amount: Mapped[int] = mapped_column(nullable=False, unique=False)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone('EST')), nullable=False)
    
    def __repr__(self):
        return f"Transaction(item_price={self.item_price}, amount={self.amount}, timestamp={self.timestamp})"