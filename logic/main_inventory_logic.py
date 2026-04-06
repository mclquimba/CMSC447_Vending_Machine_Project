from sqlalchemy import select
from sqlalchemy.orm import Session

from classes.item import Item
from classes.main_inventory import MainInventory
from utilities.error_checking import ErrorChecking as check

def add_stock(session: Session, id: str, quantity: str) -> MainInventory:
    errors = {}
    errors_id = []
    errors_quantity = []

    strip_id = id.strip()
    strip_quantity = quantity.strip()

    check.check_id_nop(strip_id, errors_id)
    check.check_quantity_nop(strip_quantity, errors_quantity)
    
    for field, field_errors in (("id", errors_id), ("quantity", errors_quantity)):
        if field_errors:
            errors[field] = field_errors

    if errors:
        raise ValueError(errors)
    
    int_id = int(strip_id)
    int_quantity = int(strip_quantity)
    
    item = session.get(Item, int_id)
    if item is None:
        raise ValueError({"id": [f"Item {int_id} not found."]})
    
    if item.main_inventory is None:
        item.main_inventory = MainInventory(item_id=int_id, quantity=int_quantity)
    else:
        item.main_inventory.quantity += int_quantity

    session.flush()
    
    return item.main_inventory

def get_stock(session: Session, id: str) -> MainInventory:
    errors = {}
    errors_id = []

    strip_id = id.strip()
    
    check.check_id_nop(strip_id, errors_id)
    if errors_id:
        errors["item_id"] = errors_id
        raise ValueError(errors)
    
    int_id = int(strip_id)

    item = session.get(Item, int_id)
    if item is None:
        raise ValueError({"id": [f"Item {int_id} not found."]})
    if item.main_inventory is None:
        raise ValueError({"id": [f"Item {int_id} not found in the main inventory."]})
    
    return item.main_inventory

def display_low_stock(session: Session) -> list[MainInventory]:
    query = select(MainInventory).join(Item).order_by(Item.name).where(MainInventory.quantity < MainInventory.low_stock_threshold)
    return list(session.scalars(query))

def search_stock(session: Session, )