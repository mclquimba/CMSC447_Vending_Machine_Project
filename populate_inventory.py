from database import Session
import logic.vm_slot_logic as vm
from tables.vm_slot import VendingMachineSlot, Status


def ensure_slot(session, slot_value):
    """
    Makes sure the slot exists before updating it.
    This helps because your current seed file has no D3 or F6,
    but your vending machine notes mention those slots.
    """
    errors = []
    slot = vm.get_slot(session, slot_value, errors)

    if slot is None:
        slot = VendingMachineSlot(
            item_name=None,
            item_price=None,
            slot_value=slot_value,
            status=Status.OUT,
            quantity_cur=0,
            quantity_max=10,
            threshold=3
        )
        session.add(slot)
        session.flush()

    return slot


stock_updates = [
    # slot, item name, price, quantity, threshold

    # A row
    ("A0", "", "", "0", "3"),  # Empty
    ("A2", "Eraser", "5.00", "1", "3"),
    ("A4", "", "", "0", "3"),  # Empty
    ("A6", "Mini Stapler", "4.10", "1", "3"),

    # B row
    ("B0", "Pens", "3.10", "2", "3"),
    ("B2", "Post-it Notes", "4.50", "2", "3"),
    ("B4", "Paper Mate Lead Pencils", "8.00", "1", "3"),
    ("B6", "Markers", "3.00", "2", "3"),

    # C row
    ("C0", "First Aid Kit", "5.05", "3", "3"),
    ("C2", "", "", "0", "3"),  # Empty
    ("C4", "", "", "0", "3"),  # Empty
    ("C6", "", "", "0", "3"),  # Empty

    # D row
    ("D0", "Mini Tissues", "1.00", "4", "3"),
    ("D1", "Afrin", "13.00", "6", "3"),
    ("D3", "DayQuil", "4.00", "1", "3"),
    ("D4", "NyQuil", "4.05", "1", "3"),
    ("D6", "Pepcid Complete", "5.10", "5", "3"),

    # E row
    ("E1", "Advil", "3.05", "5", "3"),
    ("E2", "On/Go", "12.00", "1", "3"),
    ("E4", "Benadryl", "5.15", "4", "3"),
    ("E6", "", "", "0", "3"),  # Empty

    # F row
    ("F0", "Trojan ENZ", "4.15", "2", "3"),
    ("F2", "My Way", "13.05", "1", "3"),
    ("F4", "Tampax", "6.00", "1", "3"),
    ("F6", "", "", "0", "3"),  # Empty / Travel Kit slot
]


def main():
    with Session() as session:
        try:
            for slot_value, item_name, item_price, quantity_cur, threshold in stock_updates:
                ensure_slot(session, slot_value)

                vm.manual(
                    session,
                    slot_value,
                    item_name,
                    item_price,
                    quantity_cur,
                    threshold
                )

            session.commit()
            print("Inventory populated successfully.")

        except ValueError as e:
            session.rollback()
            print("Validation error:", e)

        except Exception as e:
            session.rollback()
            print("Unexpected error:", e)


if __name__ == "__main__":
    main()