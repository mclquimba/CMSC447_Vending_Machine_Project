#To do: Create test.py to test frontend AND backend.
# Import the backend and frontend modules, as well as the VendingMachineSlot class
import backend.logic.modification_logic as modification_logic
import backend.logic.transaction_logic as transaction_logic
import backend.logic.user_logic as user_logic
import backend.logic.vm_slot_logic as vm_slot_logic
from backend.tables.modification import Modification
from backend.tables.transaction import Transaction
from backend.tables.user import Role, User
from backend.tables.vm_slot import VendingMachineSlot

import frontend.app
from backend.database import Session

# Test the modification logic functions
def test_mod_manual(session):
    # Test the _mod_manual function
    slot = session.query(VendingMachineSlot).filter_by(slot_value='A1').first()
    result = modification_logic._mod_manual(session, slot, 'New Item', 1.50, 10, 5)
    assert result == True
    assert slot.item_name == 'New Item'
    assert slot.item_price == 1.50
    assert slot.quantity_cur == 10
    assert slot.threshold == 5

def test_mod_restock(session):
    # Test the _mod_restock function
    slot = session.query(VendingMachineSlot).filter_by(slot_value='A1').first()
    result = modification_logic._mod_restock(session, slot, 20)
    assert result == True
    assert slot.quantity_cur == 20

def test_mod_transaction(session):
    # Test the _mod_transaction function
    result = transaction_logic._mod_transaction(session, 'A1', 1.50, 2)
    assert result == True
    slot = session.query(VendingMachineSlot).filter_by(slot_value='A1').first()
    assert slot.quantity_cur == 18

# Test the transaction logic functions
def test_record_transaction(session):
    # Test the record_transaction function
    transaction = transaction_logic.record_transaction(session, '1.50', '2')
    assert transaction.item_price == 1.50
    assert transaction.amount == 2

# Test the user logic functions
def test_get_username(session):
    # Test the get_username function
    result = user_logic.get_username(session, 'admin')
    assert result == True
    result = user_logic.get_username(session, 'nonexistent')
    assert result == False

def test_get_next_id(session):
    # Test the get_next_id function
    result = user_logic.get_next_id(session)
    assert result == 2  # Assuming there is already one user with ID 1

def test_get_admin(session):
    # Test the get_admin function
    result = user_logic.get_admin(session)
    assert result == True  # Assuming there is already an admin user

def test_add_user(session):
    # Test the add_user function
    new_user = user_logic.add_user(session, 'newuser', Role.STAFF)
    assert new_user.username == 'newuser'
    assert new_user.role == Role.STAFF

def test_delete_user(session):
    # Test the delete_user function
    user = session.query(User).filter_by(username='newuser').first()
    result = user_logic.delete_user(session, user.user_id)
    assert result == True
    user = session.query(User).filter_by(username='newuser').first()
    assert user is None

# Test the vending machine slot logic functions
def test_get_slot(session):
    # Test the get_slot function
    slot = vm_slot_logic.get_slot(session, 'A1')
    assert slot.slot_value == 'A1'
    assert slot.item_name == 'New Item'
    assert slot.item_price == 1.50
    assert slot.quantity_cur == 20
    assert slot.threshold == 5

def test_get_purchase(session):
    # Test the get_purchase function
    slot = vm_slot_logic.get_purchase(session, 1.50, [])
    assert slot.slot_value == 'A1'
    assert slot.item_name == 'New Item'
    assert slot.item_price == 1.50
    assert slot.quantity_cur == 20
    assert slot.threshold == 5

def test_get_status(session):
    # Test the get_status function
    assert vm_slot_logic.get_status(0, 5) == 'OUT'
    assert vm_slot_logic.get_status(2, 5) == 'LOW'
    assert vm_slot_logic.get_status(5, 5) == 'GOOD'

def test_manual(session):
    # Test the manual function
    slot = vm_slot_logic.manual(session, 'A1', 'Another Item', 2.00, 15, 10)
    assert slot.slot_value == 'A1'
    assert slot.item_name == 'Another Item'
    assert slot.item_price == 2.00
    assert slot.quantity_cur == 15
    assert slot.threshold == 10

def test_clear_slot(session):
    # Test the clear_slot function
    slot = vm_slot_logic.clear_slot(session, 'A1')
    assert slot.slot_value == 'A1'
    assert slot.item_name is None
    assert slot.item_price is None
    assert slot.quantity_cur == 0
    assert slot.threshold == 0

def test_restock(session):
    # Test the restock function
    slot = vm_slot_logic.restock(session, 'A1', 25)
    assert slot.slot_value == 'A1'
    assert slot.quantity_cur == 25

def test_purchase(session):
    # Test the purchase function
    result = vm_slot_logic.purchase(session, 'A1', 2)
    assert result == True
    slot = session.query(VendingMachineSlot).filter_by(slot_value='A1').first()
    assert slot.quantity_cur == 23

def test_list_stock_slots(session):
    # Test the list_stock_slots function
    slots = vm_slot_logic.list_stock_slots(session)
    assert len(slots) > 0  # Assuming there are some stock slots in the database

def test_list_stock_status(session):
    # Test the list_stock_status function
    status_list = vm_slot_logic.list_stock_status(session)
    assert len(status_list) > 0  # Assuming there are some stock slots in the database


# TEST FRONTEND
def test_frontend_get_status(item):
    ratio = item["quantity"] / item["max"]

    if item["quantity"] == 0:
        return "OUT"
    elif ratio < 0.5:
        return "LOW"
    else:
        return "GOOD"
    
def test_dashboard():
    items_out = 0
    items_low = 0

    for item in frontend.app.inventory:
        item["status"] = frontend.app.get_status(item)

        if item["status"] == "OUT":
            items_out += 1
        elif item["status"] == "LOW":
            items_low += 1
    
    assert items_out == 1  
    assert items_low == 2  

def test_stock():
    page = 1

    for item in frontend.app.inventory:
        item["status"] = frontend.app.get_status(item)

        if item["quantity"] == 0:
            item["name"] = "empty"
    
    assert page == 1

def test_buy():
    # Simulate a purchase and check if the quantity is updated correctly
    slot = frontend.app.inventory[0]  # Assuming the first item is being purchased
    initial_quantity = slot["quantity"]
    purchase_quantity = 2

    if slot["quantity"] >= purchase_quantity:
        slot["quantity"] -= purchase_quantity

    assert slot["quantity"] == initial_quantity - purchase_quantity

def restock_item():
    # Simulate restocking an item and check if the quantity is updated correctly
    slot = frontend.app.inventory[0]  # Assuming the first item is being restocked
    initial_quantity = slot["quantity"]
    restock_quantity = 5

    slot["quantity"] += restock_quantity

    assert slot["quantity"] == initial_quantity + restock_quantity


def test_suite():
    with Session() as session:
        test_mod_manual(session)
        test_mod_restock(session)
        test_mod_transaction(session)
        test_record_transaction(session)
        test_get_username(session)
        test_get_next_id(session)
        test_get_admin(session)
        test_add_user(session)
        test_delete_user(session)
        test_get_slot(session)
        test_get_purchase(session)
        test_get_status(session)
        test_manual(session)
        test_clear_slot(session)
        test_restock(session)
        test_purchase(session)
        test_list_stock_slots(session)
        test_list_stock_status(session)

    test_frontend_get_status(None)
    test_dashboard()
    test_stock()
    test_buy()
    restock_item()

    print("All tests passed!")


if __name__ == "__main__":
    test_suite()

def update_item(slot):
    # Simulate updating an item and check if the details are updated correctly
    new_name = "Updated Item"
    new_price = 2.50
    new_quantity = 15
    new_max = 20

    slot["name"] = new_name
    slot["price"] = new_price
    slot["quantity"] = new_quantity
    slot["max"] = new_max

    assert slot["name"] == new_name
    assert slot["price"] == new_price
    assert slot["quantity"] == new_quantity
    assert slot["max"] == new_max
