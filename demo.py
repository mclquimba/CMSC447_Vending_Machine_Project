from database import Session
import logic.item_logic as logic_item
import logic.main_inventory_logic as logic_main
import logic.vending_machine_slot_logic as logic_vm

DEMO_OPTIONS = ["Add Item", 
                "Delete Item", 
                "Add Item to Main Inventory",
                "Assign Item to Vending Machine Slot",
                "Unassign Item from Vending Machine Slot",
                "Make Transaction",
                "Restock Vending Machine Slot",
                "Restock Item in Main Inventory",
                "Quit"]

def display_items(items):
    if not items:
        print("No items in the database.")
        return False
    
    for item in items:
        print(item)
        
    print()

    return True

def display_slots(slots):
    if not slots:
        print("No assigned slots.")
        return False
    
    for slot in slots:
        print(slot)

    print()

    return True

def display_items_main(items_main):
    if not items_main:
        print("No Items in Main Inventory.")
        return False
    
    for item_main in items_main:
        print(item_main)

    print()
    
    return True

def demo_create_item(session):
    name = input("Enter Item Name: ").strip()
    category = input("Enter Item Category: ").strip()
    price = input("Enter Item Price: ").strip()
    print()

    try:
        logic_item.create_item(session, name, price, category)
        session.commit()
        print("Item created.")
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ": ", field_errors)

    print()

    return

def demo_delete_item(session):
    
    items = logic_item.search_items(session, string=None)
    if not display_items(items):
        return

    id_num = input("Enter Item's ID to delete: ").strip()
    print()

    try:
        logic_item.delete_item(session, id_num)
        session.commit()
        print("Item deleted.")
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ": ", field_errors)

    print()

    return

def demo_add_stock(session):
    items = logic_item.search_items(session, string=None)
    
    if not display_items(items):
        return
    
    id_num = input("Enter Item ID: ").strip()
    quantity = input("Enter Item Quantity: ").strip()
    threshold = input("Enter Item Stock Threshold: ").strip()
    print()
    
    try:
        logic_main.add_stock(session, id_num, quantity, threshold)
        session.commit()
        print("Item added to Main Inventory.")
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ": ", field_errors)

    print()
        
    return

def demo_assign_slot(session):
    items = logic_item.search_items(session, string=None)
    
    if not display_items(items):
        return
    
    # ID, slot value, quantity, threshold
    
    id_num = input("Enter Item ID: ").strip()
    slot_value = input("Enter Slot Value: ").strip()
    quantity = input("Enter Item Quantity: ").strip()
    threshold = input("Enter Item VM Threshold: ").strip()
    print()
    
    try:
        logic_vm.assign_slot(session, id_num, slot_value, quantity, threshold)
        session.commit()
        print(f"Item assigned to Vending Machine Slot {slot_value.strip().upper()}.")
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ": ", field_errors)

    print()
            
    return

def demo_unassign_slot(session):
    slots = logic_vm.list_slots(session)

    if not display_slots(slots):
        return
    
    slot_value = input("Enter Slot Value: ").strip()
    print()
    
    try:
        logic_vm.unassign_slot(session, slot_value)
        session.commit()
        print(f"Item unassigned from Vending Machine Slot {slot_value.strip().upper()}.")
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ": ", field_errors)

    print()

    return

def demo_transaction(session):
    slots = logic_vm.list_slots(session)

    if not display_slots(slots):
        return
    
    slot_value = input("Enter Slot Value: ").strip()
    quantity = input("Enter Amount: ").strip()
    print()

    try:
        logic_vm.transaction(session, slot_value, quantity)
        session.commit()
        print("Transaction occured.")
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ": ", field_errors)

    print()

    return

def demo_restock_vm(session):
    slots = logic_vm.list_slots(session)

    if not display_slots(slots):
        return
    
    slot_value = input("Enter Slot Value: ").strip()
    change = input("Enter Amount: ").strip()
    print()

    try:
        logic_vm.restock_slot(session, slot_value, change)
        session.commit()
        print(f"Slot {slot_value.strip().upper()} restocked.")
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ": ", field_errors)

    print()
        
    return

def demo_restock_main(session):
    items_main = logic_main.search_stock(session, string=None)

    if not display_items_main(items_main):
        return
    
    id_num = input("Enter Item ID: ").strip()
    change = input("Enter Amount: ").strip()
    print()

    try:
        logic_main.restock(session, id_num, change)
        session.commit()
        print(f"Item {id_num} restocked.")
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ": ", field_errors)

    print()

    return

def main():
    while True:
        with Session() as session:
            for i, demo_option in enumerate(DEMO_OPTIONS, start=1):
                print(f"{i}: {demo_option}")
            print()

            option = input("Enter Option: ").strip()

            if option == "1":
                demo_create_item(session)
            elif option == "2":
                demo_delete_item(session)
            elif option == "3":
                demo_add_stock(session)
            elif option == "4":
                demo_assign_slot(session)
            elif option == "5":
                demo_unassign_slot(session)
            elif option == "6":
                demo_transaction(session)
            elif option == "7":
                demo_restock_vm(session)
            elif option == "8":
                demo_restock_main(session)
            elif option == "9":
                break
            else:
                print("Invalid Option.\n")
    return

if __name__ == "__main__":
    main()