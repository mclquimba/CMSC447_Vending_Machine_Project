from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from classes import Base

MAX_SLOT_VAL = 10
DEFAULT_CAP = 10
DEFAULT_THRESH_VM = 3
DEFAULT_QUANTITY_VM = 0

class VendingMachineSlot(Base):
    __tablename__ = "vending_machine_slots"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[Optional[int]] = mapped_column(ForeignKey("items.id", ondelete="SET NULL"), nullable=True)
    slot_value: Mapped[str] = mapped_column(String(MAX_SLOT_VAL), unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(default=DEFAULT_QUANTITY_VM, nullable=False)
    cap: Mapped[int] = mapped_column(default=DEFAULT_CAP, nullable=False)
    low_stock_threshold: Mapped[int] = mapped_column(default=DEFAULT_THRESH_VM, nullable=False)

    item: Mapped["Item"] = relationship("Item", back_populates="vending_machine_slots", passive_deletes=True)
    modifications: Mapped[List["Modification"]] = relationship("Modification", back_populates="vending_machine_slot")

    def __repr__(self):
        string = ""
        if self.item is None:
            string = f"VendingMachineSlot(item=None, slot_value={self.slot_value}, vm_quantity={self.quantity}, vm_cap={self.cap}, vm_low_stock_threshold={self.low_stock_threshold})"
        else:
            string = f"VendingMachineSlot(item_id={self.item.id_num}, item_name={self.item.name}, slot_value={self.slot_value}, vm_quantity={self.quantity}, vm_cap={self.cap}, vm_low_stock_threshold={self.low_stock_threshold})"
        return string