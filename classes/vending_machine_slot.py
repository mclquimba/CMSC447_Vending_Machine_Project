from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from classes.base import Base

MAX_SLOT_VAL = 10

class VendingMachineSlot(Base):
    __tablename__ = "vending_machine_slots"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[Optional[int]] = mapped_column(ForeignKey("items.id", ondelete="SET NULL"), nullable=True)
    slot_value: Mapped[str] = mapped_column(String(MAX_SLOT_VAL), unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(default=0, nullable=False)
    cap: Mapped[int] = mapped_column(default=10, nullable=False)
    low_stock_threshold: Mapped[int] = mapped_column(default=3, nullable=False)

    item: Mapped["Item"] = relationship(back_populates="vending_machine_slots", passive_deletes=True)
    modifications: Mapped[List["Modification"]] = relationship(back_populates="vending_machine_slot")

    def __repr__(self):
        return f"VendingMachineSlot(item_id={self.item_id}, slot_value={self.slot_value}, quantity={self.quantity}, low_stock_threshold={self.low_stock_threshold})"