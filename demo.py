from database import Session
import logic.vm_slot_logic as vm
import logic.transaction_logic as transac

OPTIONS = [
    "Modify Slot",
    "Clear Slot",
    "Restock Slot",
    "Purchase Item",
    "List Stock (Slot Label)",
    "List Low Stock (Status)",
    "Quit"
]

def initiate(function, session, option):
    ret = True
    print()
    try:
        function()
        session.commit()
        print(f"{OPTIONS[option]} Success")
        ret = True
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ":", field_errors)
            ret = False
    print()
    return ret

def initiate_minus(function, session):
    print()
    try:
        function()
        session.commit()
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ":", field_errors)
    print()
    return

def demo_manual(session):
    demo_list_stock_slot(session)
    
    slot_value = input("Enter Slot Value: ").strip()
    item_name = input("Enter Item Name: ").strip()
    item_price = input("Enter Item Price: ").strip()
    quantity_cur = input("Enter Current Quantity: ").strip()
    threshold = input("Enter threshold: ").strip()
    
    initiate(lambda: vm.manual(session, slot_value, item_name, item_price, quantity_cur, threshold), session, 0)
            
    return True
        
def demo_clear_slot(session):
    demo_list_stock_slot(session)
    
    slot_value = input("Enter Slot Value: ").strip()
    
    initiate(lambda: vm.clear_slot(session, slot_value), session, 1)
    
    return True
    
def demo_restock(session):
    demo_list_stock_slot(session)
    
    slot_value = input("Enter Slot Value: ")
    amount = input("Enter Restock Amount: ")
    
    initiate(lambda: vm.restock(session, slot_value, amount), session, 2)
    
    return True
    
def demo_purchase(session):
    demo_list_stock_slot(session)
    
    price = input("Enter Price: ")
    amount = input("Enter Amount: ")
    
    ret = initiate(lambda: vm.purchase(session, price, amount), session, 3)
    if ret:
        initiate_minus(lambda: transac.record_transaction(session, price, amount), session)
    
    return True
    
def demo_list_stock_slot(session):
    slots = vm.list_stock_slot(session)
    print()
    for slot in slots:
        print(slot)
    print()
    return True
    
def demo_list_stock_status(session):
    slots = vm.list_stock_status(session)
    print()
    for slot in slots:
        print(slot)
    print()
    return True

def main():
    while True:
        with Session() as session:
            for i, option in enumerate(OPTIONS, start=1):
                print(f"{i}. {option}")
            print()
            
            option = input("Enter Option: ").strip()
            
            if option == "1":
                demo_manual(session)
            elif option == "2":
                demo_clear_slot(session)
            elif option == "3":
                demo_restock(session)
            elif option == "4":
                demo_purchase(session)
            elif option == "5":
                demo_list_stock_slot(session)
            elif option == "6":
                demo_list_stock_status(session)
            elif option == "7":
                break
            else:
                print()
                print("Invalid option.")
                print()
    return

if __name__ == "__main__":
    main()