from sqlalchemy import select, delete

import logic.user_logic as u
import logic.vm_slot_logic as v

from tables.vm_slot import Status
from tables.vm_slot import VendingMachineSlot as V
from tables.modification import Modification as M

from tables.user import Role, User

from database import Session
from seed import SLOT_VALUES

def clear_mods(session):
    session.execute(delete(M))
    session.commit()

def test_manual_and_clear(session):
    # TC001
    # Testing add item
    v.manual(session, "A0", "Item", "2.00", "3", "3")
    session.commit()
    if v.get_slot(session, "A0", []).item_name != "Item":
        print("TC001: FAIL")
        v.clear_slot(session, "A0")
        session.commit()
        return
    else:
        print("TC001: PASS")

    # TC002
    # Testing modify item
    v.manual(session, "A0", "Change", "3.00", "5", "4")
    session.commit()
    slot = v.get_slot(session, "A0", [])
    if slot.item_name != "Change" and slot.quantity_cur != 5 and slot.threshold != 4 and slot.status != Status.GOOD and slot.item_price != 3.00:
        print("TC002: FAIL")
    else:
        print("TC002: PASS")
    
    # TC003
    # Testing status change
    v.manual(session, "A0", "Nothing", "3.00", "0", "3")
    session.commit()
    slot = v.get_slot(session, "A0", [])
    if slot.status != Status.OUT:
        print("TC003: FAIL")
    else:
        print("TC003: PASS")
    
    # TC004
    # Testing slot not modified when no name
    try:
        v.manual(session, "A0", "", "3.00", "0", "3")
        print("TC004: FAIL")
    except ValueError:
        if v.get_slot(session, "A0", []).item_name is None:
            print("TC004: FAIL")
        else:
            print("TC004: PASS")

    # TC005
    # Testing slot not modified when no price
    try:
        v.manual(session, "A0", "Nothing", "", "0", "3")
        print("TC005: FAIL")
    except ValueError:
        if v.get_slot(session, "A0", []).item_name is None:
            print("TC005: FAIL")
        else:
            print("TC005: PASS")

    # TC006
    # Testing slot quantity == 0 when both name and price is None
    v.manual(session, "A0", "Initialize", "2.00", "3", "3")
    v.manual(session, "A0", "", "", "3", "3")
    if v.get_slot(session, "A0", []).quantity_cur != 0:
        print("TC006: FAIL")
    else:
        print("TC006: PASS")

    # TC007
    # Testing slot not modified when invalid quantity
    try:
        v.manual(session, "A0", "Initialize", "2.00", "-1", "3")
        print("TC007: FAIL")
    except ValueError:
        if v.get_slot(session, "A0", []).quantity_cur == -1:
            print("TC007: FAIL")
        else:
            print("TC007: PASS")

    # TC008
    # Testing slot not modified when invalid price
    try:
        v.manual(session, "A0", "Initialize", "-2.00", "3", "3")
        print("TC008: FAIL")
    except ValueError:
        if v.get_slot(session, "A0", []).item_price == -2.00:
            print("TC008: FAIL")
        else:
            print("TC008: PASS")

    # TC009
    # Testing slot not modified when invalid threshold
    try:
        v.manual(session, "A0", "Initialize", "2.00", "3", "0")
        print("TC009: FAIL")
    except ValueError:
        if v.get_slot(session, "A0", []).threshold == 0:
            print("TC009: FAIL")
        else:
            print("TC009: PASS")

    # TC010
    # Testing clear slot
    v.clear_slot(session, "A0")
    session.commit()
    slot = v.get_slot(session, "A0", [])
    if slot.item_name is not None or slot.item_price is not None or slot.quantity_cur != 0:
        print("TC010: FAIL")
    else:
        print("TC010: PASS")

    clear_mods(session)
    return

def test_restock(session):
    # TC011
    # Testing restock occurs on empty slot
    v.restock(session, "A0", "3")
    session.commit()
    if v.get_slot(session, "A0", []).quantity_cur != 0:
        print("TC011: FAIL")
    else:
        print("TC011: PASS")

    # TC012
    # Testing restock occurs when item exists
    v.manual(session, "A0", "Item", "2.00", "2", "4")
    session.commit()
    v.restock(session, "A0", "3")
    session.commit()
    if v.get_slot(session, "A0", []).quantity_cur != 5:
        print("TC012: FAIL")
    else:
        print("TC012: PASS")

    # TC013
    # Testing restock occurs when amount added to quantity exceeds max
    try:
        v.restock(session, "A0", "100")
        print("TC013: FAIL")
    except ValueError:
        if v.get_slot(session, "A0", []).quantity_cur >= 100:
            print("TC013: FAIL")
        else:
            print("TC013: PASS")

    # TC014
    # Testing restock doesn't occurs when amount is invalid
    try:
        v.restock(session, "A0", "-100")
        print("TC014: FAIL")
    except ValueError:
        if v.get_slot(session, "A0", []).quantity_cur < 0:
            print("TC014: FAIL")
        else:
            print("TC014: PASS")

    v.clear_slot(session, "A0")
    session.commit()
    
    clear_mods(session)
    return

def test_purchase(session):
    # TC015
    # Testing purchase occurs when amount < quantity
    v.manual(session, "A0", "Item", "2.00", "8", "3")
    session.commit()
    v.purchase(session, "2.00", "3")
    session.commit()
    if v.get_slot(session, "A0", []).quantity_cur != 5:
        print("TC015: FAIL")
    else:
        print("TC015: PASS")

    # TC016
    # Testing purchase fails when amount == quantity
    v.manual(session, "A0", "Item", "2.00", "8", "3")
    session.commit()
    v.purchase(session, "2.00", "8")
    session.commit()
    if v.get_slot(session, "A0", []).quantity_cur != 0:
        print("TC016: FAIL")
    else:
        print("TC016: PASS")


    # TC017
    # Testing purchase fails when amount > quantity
    v.manual(session, "A0", "Item", "2.00", "8", "3")
    session.commit()
    try:
        v.purchase(session, "2.00", "100")
        print("TC017: FAIL")
    except ValueError:
        if v.get_slot(session, "A0", []).quantity_cur < 0:
            print("TC017: FAIL")
        else:
            print("TC017: PASS")

    # TC018
    # Testing purchase fails when amount is invalid
    v.manual(session, "A0", "Item", "2.00", "8", "3")
    session.commit()
    try:
        v.purchase(session, "2.00", "-20")
        print("TC018: FAIL")
    except ValueError:
        if v.get_slot(session, "A0", []).quantity_cur != 8:
            print("TC018: FAIL")
        else:
            print("TC018: PASS")

    v.clear_slot(session, "A0")
    session.commit()

    clear_mods(session)
    return

def test_display(session):
    v.manual(session, "A0", "Item1", "2.00", "3", "3")
    v.manual(session, "A2", "Item2", "2.50", "8", "3")
    v.manual(session, "A4", "Item3", "3.00", "0", "3")
    v.manual(session, "A6", "Item4", "3.50", "2", "3")
    v.manual(session, "B0", "Item5", "4.00", "10", "3")
    v.manual(session, "B2", "Item6", "4.50", "0", "3")
    session.commit()

    # TC019
    # Testing list slots
    inventory = v.list_stock_slot(session)
    if len(inventory) != 24:
        print("TC019: FAIL")
    else:
        print("TC019: PASS")

    # TC020
    # Testing list slots based on status, expect 4 results
    inventory = v.list_stock_status(session)
    if len(inventory) != 6:
        print("TC020: FAIL")
    else:
        print("TC020: PASS")

    for slot in SLOT_VALUES:
        v.clear_slot(session, slot)
        session.commit()

    clear_mods(session)
    return

def test_user(session):
    # TC021
    # Testing if add user works
    u.add_user(session, "Name1", Role.ADMIN)
    u.add_user(session, "Name2", Role.STAFF)
    session.commit()
    query = select(User).order_by(User.id)
    if len(session.scalars(query).all()) != 2:
        print("TC021: FAIL")
    else:
        print("TC021: PASS")

    #TC022
    # Testing if delete user works
    u.delete_user(session, "1")
    u.delete_user(session, "2")
    session.commit()
    query = select(User).order_by(User.id)
    if session.scalars(query).all():
        print("TC022: FAIL")
    else:
        print("TC022: PASS")

    clear_mods(session)
    return

def main():
    with Session() as session:
        for slot in SLOT_VALUES:
            v.clear_slot(session, slot)

        test_manual_and_clear(session)
        print()

        test_restock(session)
        print()

        test_purchase(session)
        print()

        test_display(session)
        print()

        test_user(session)
        print()

if __name__ == "__main__":
    main()