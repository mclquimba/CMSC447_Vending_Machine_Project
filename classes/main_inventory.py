from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from classes.base import Base


DEFAULT_QUANTITY = 0
DEFAULT_THRESH = 10

class MainInventory(Base):
    __tablename__ = "main_inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), nullable=False, unique=True)
    quantity: Mapped[int] = mapped_column(default=0, nullable=False)
    low_stock_threshold: Mapped[int] = mapped_column(default=10, nullable=False)

    item: Mapped["Item"] = relationship("Item", back_populates="main_inventory", passive_deletes=True)

    def __repr__(self):
        return f"MainInventory(item_id={self.item_id}, quantity={self.quantity}, low_stock_threshold={self.low_stock_threshold})"