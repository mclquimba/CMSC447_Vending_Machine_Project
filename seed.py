from sqlalchemy import select, func
from database import Session, engine
from classes.vending_machine_slot import VendingMachineSlot, DEFAULT_CAP, DEFAULT_QUANTITY_VM, DEFAULT_THRESH_VM
from classes.base import Base
from classes.item import Item
from classes.main_inventory import MainInventory
from classes.inventory_modifications import Modification

SLOT_VALUES = [
    "A0", "A2", "A4", "A6",
    "B0", "B2", "B4", "B6",
    "C0", "C2", "C4", "C6",
    "D0", "D2", "D4", "D6",
    "E0", "E2", "E4", "E6",
    "F0", "F2", "F4", "F6"
]

def seed_slots(session):
    count = session.scalar(select(func.count(VendingMachineSlot.id)))

    if count == 24:
        print("All slots exist.")
        return
    
    session.query(VendingMachineSlot).delete()
    session.commit()
    
    for label in SLOT_VALUES:
        slot = VendingMachineSlot(item_id=None, slot_value=label, quantity=DEFAULT_QUANTITY_VM, cap=DEFAULT_CAP, low_stock_threshold=DEFAULT_THRESH_VM)
        session.add(slot)

    session.flush()
    print("Slots initialized.")

def main():
    Base.metadata.create_all(bind=engine)

    with Session() as session:
        seed_slots(session)
        session.commit()
    print("seed.py complete.")

if __name__ == "__main__":
    main()