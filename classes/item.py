from sqlalchemy import DECIMAL, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from classes.base import Base
from decimal import Decimal
from typing import List

MAX_NAME = 200
MAX_CAT = 100

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(MAX_NAME), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    category: Mapped[str] = mapped_column(String(MAX_CAT), nullable=False)
    
    # created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(TimeZone("America/New_York")))

    vending_machine_slots: Mapped[List["VendingMachineSlot"]] = relationship("VendingMachineSlot", back_populates="item", passive_deletes=True)
    main_inventory: Mapped["MainInventory"] = relationship("MainInventory", back_populates="item", cascade="all, delete-orphan", uselist=False, passive_deletes=True)

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name}, category={self.category}, price={self.price})"
    