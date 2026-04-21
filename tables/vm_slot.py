from sqlalchemy import String, DECIMAL, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from tables import Base
from decimal import Decimal
import enum

MAX_NAME_CHARS = 200
MAX_SLOT_CHARS = 10
DEFAULT_CUR_QUANTITY = 0
DEFAULT_MAX_QUANTITY = 10
DEFAULT_THRESHOLD = 3

class Status(enum.Enum):
    OUT = "OUT"
    LOW = "LOW"
    GOOD = "GOOD"

class VendingMachineSlot(Base):
    __tablename__ = "vending_machine_slots"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[Optional[str]] = mapped_column(String(MAX_NAME_CHARS), nullable=True)
    item_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True, unique=True)
    slot_value: Mapped[str] = mapped_column(String(MAX_SLOT_CHARS), nullable=False, unique=True)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)
    quantity_cur: Mapped[int] = mapped_column(default=DEFAULT_CUR_QUANTITY, nullable=False)
    quantity_max: Mapped[int] = mapped_column(default=DEFAULT_MAX_QUANTITY, nullable=False)
    threshold: Mapped[int] = mapped_column(default=DEFAULT_THRESHOLD, nullable=False)
    
    def __repr__(self):
        name = "None" if self.item_name is None else self.item_name
        price = "None" if self.item_price is None else self.item_price
        
        return f"VendingMachineSlot(slot_value={self.slot_value}, item_name={name}, item_price={price}, status={self.status}, quantity_cur={self.quantity_cur}, quantity_max={self.quantity_max}, threshold={self.threshold})"