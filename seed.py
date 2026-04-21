from sqlalchemy import select, func
from database import Session, engine
from tables.vm_slot import VendingMachineSlot, DEFAULT_MAX_QUANTITY, DEFAULT_CUR_QUANTITY, DEFAULT_THRESHOLD, Status
from tables.base import Base

SLOT_VALUES = [
    "A0", "A2", "A4", "A6",
    "B0", "B2", "B4", "B6",
    "C0", "C2", "C4", "C6",
    "D0", "D1", "D4", "D6",
    "E0", "E2", "E4", "E6",
    "F0", "F2", "F3", "F4"
]

def seed_slots(session):
    query = select(func.count(VendingMachineSlot.id))
    count = session.scalar(query)
    
    if count == len(SLOT_VALUES):
        print("All slots exist.")
        return
    
    session.query(VendingMachineSlot).delete()
    session.commit()
    
    for label in SLOT_VALUES:
        slot = VendingMachineSlot(item_name=None, item_price=None, slot_value=label, status=Status.OUT, quantity_cur=DEFAULT_CUR_QUANTITY, quantity_max=DEFAULT_MAX_QUANTITY, threshold=DEFAULT_THRESHOLD)
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