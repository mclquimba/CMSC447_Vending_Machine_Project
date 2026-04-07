from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import enum
from classes.base import Base
from datetime import datetime, timezone

class ModSource(enum.Enum):
    VM_SLOT = "vending_machine_slot"
    MAIN_INVENTORY = "main_inventory"

class ModType(enum.Enum):
    TRANSACTION = "transaction"
    RESTOCK = "restock"
    MANUAL = "manual"

class Modification(Base):
    __tablename__ = "modifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    slot_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vending_machine_slots.id", ondelete="SET NULL"), nullable=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="SET NULL"), nullable=True)
    source: Mapped[ModSource] =  mapped_column(Enum(ModSource), nullable=False)
    mod_type: Mapped[ModType] = mapped_column(Enum(ModType), nullable=False)
    quantity_start: Mapped[int] = mapped_column()
    quantity_final: Mapped[int] = mapped_column()
    threshold: Mapped[int] = mapped_column(nullable=False)
    time: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False)

    vending_machine_slot: Mapped[Optional["VendingMachineSlot"]] = relationship("VendingMachineSlot", back_populates="modifications", passive_deletes=True)
    item: Mapped["Item"] = relationship("Item", passive_deletes=True)

    def __repr__(self):
        return f"Modification(id={self.id}, source={self.source}, type={self.mod_type}, quantity_change={self.quantity_start}, quantity_final={self.quantity_final})"