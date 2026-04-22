from sqlalchemy import Enum, DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pytz import timezone
import enum

from tables import Base

MAX_NAME_CHARS = 200
MAX_SLOT_CHARS = 10

class ModType(enum.Enum):
    RESTOCK = "restock"
    MANUAL = "manual"
    TRANSACTION = "transaction"

class Modification(Base):
    __tablename__ = "modifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    slot_value: Mapped[str] = mapped_column(String(MAX_SLOT_CHARS), nullable=False, unique=False)
    type: Mapped[ModType] = mapped_column(Enum(ModType), nullable=False)
    old_item_name: Mapped[Optional[str]] = mapped_column(String(MAX_NAME_CHARS), nullable=True)
    new_item_name: Mapped[Optional[str]] = mapped_column(String(MAX_NAME_CHARS), nullable=True)
    old_item_price: Mapped[Optional[Decimal]] = mapped_column()
    new_item_price: Mapped[Optional[Decimal]] = mapped_column()
    old_quantity_cur: Mapped[int] = mapped_column(nullable=False)
    new_quantity_cur: Mapped[int] = mapped_column(nullable=False)
    old_threshold: Mapped[int] = mapped_column(nullable=False)
    new_threshold: Mapped[int] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone('EST')), nullable=False)
    
    def __repr__(self):
        item_name_old = "None" if self.old_item_name is None else self.old_item_name
        item_name_new = "None" if self.new_item_name is None else self.new_item_name
        item_price_old = "None" if self.old_item_price is None else self.old_item_price
        item_price_new = "None" if self.new_item_price is None else self.new_item_price
        
        return f"Modification(\nslot_value={self.slot_value},\nold_item_name={item_name_old},\nnew_item_name={item_name_new},\nold_item_price={item_price_old},\nnew_item_price={item_price_new},\nold_quantity_cur={self.old_quantity_cur},\nnew_quantity_cur={self.new_quantity_cur}\nold_threshold={self.old_threshold},\nnew_threshold={self.new_threshold}\n,timestamp={self.timestamp}\n)"