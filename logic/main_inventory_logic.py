from sqlalchemy import select
from sqlalchemy.orm import Session

from classes.item import Item
from classes.main_inventory import MainInventory
from classes.inventory_modifications import Modification, ModSource, ModType
from utilities.error_checking import ErrorChecking as check

def add_stock(session: Session, id: str, quantity: str, threshold: str) -> MainInventory:
    errors = {}
    errors_id = []
    errors_quantity = []
    errors_threshold = []

    strip_id = id.strip()
    strip_quantity = quantity.strip()
    strip_threshold = threshold.strip()

    check.check_id_nop(strip_id, errors_id)
    check.check_quantity_nop(strip_quantity, errors_quantity)
    check.check_threshold_nop(strip_threshold, errors_threshold)
    
    for field, field_errors in (("id", errors_id), ("quantity", errors_quantity), ("threshold", errors_threshold)):
        if field_errors:
            errors[field] = field_errors

    if errors:
        raise ValueError(errors)
    
    int_id = int(strip_id)
    int_quantity = int(strip_quantity)
    int_threshold = int(strip_threshold)
    
    item = session.get(Item, int_id)
    if item is None:
        raise ValueError({"id": [f"Item {int_id} not found."]})
    
    if item.main_inventory is None:
        item.main_inventory = MainInventory(item_id=int_id, quantity=int_quantity, threshold=int_threshold)
    else:
        raise ValueError({"id": [f"Item {int_id} already exists in the main inventory."]})

    mod = Modification(slot_id=None, item_id=int_id, source=ModSource.MAIN_INVENTORY, mod_type=ModType.MANUAL, quantity_start=int_quantity, quantity_final=int_quantity, threshold=int_threshold)

    session.add(mod)
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
    check.check_item_main_inventory(item, int_id, errors_id)
    if errors_id:
        errors["id"] = errors_id
        raise ValueError(errors)
    
    return item.main_inventory

def list_low_stock(session: Session) -> list[MainInventory]:
    query = select(MainInventory).join(Item).order_by(Item.name).where(MainInventory.quantity < MainInventory.low_stock_threshold)
    return list(session.scalars(query))

def search_stock(session: Session, string: str) -> list[MainInventory]:
    query = select(MainInventory).join(Item).order_by(Item.name)
    if string:
        to_search = f"%{string.strip().lower()}%"
        query = query.where(Item.name.ilike(to_search))
    return(list(session.scalars(query)))

def restock(session: Session, id: str, change: str) -> MainInventory:
    errors = {}
    errors_id = []
    errors_change = []

    strip_id = id.strip()
    strip_change = change.strip()

    check.check_id_nop(strip_id, errors_id)
    check.check_change_nop(strip_change, errors_change)

    for field, field_errors in (("id", errors_id), ("change", errors_change)):
        if field_errors:
            errors[field] = field_errors

    if errors:
        raise ValueError(errors)

    int_id = int(strip_id)
    int_change = int(strip_change)

    item = session.get(Item, int_id)
    check.check_item_main_inventory(item, int_id, errors_id)
    if errors_id:
        errors["id"] = errors_id
        raise ValueError(errors)
    
    start_quantity = item.main_inventory.quantity
    final_quantity = item.main_inventory.quantity + int_change
    item.main_inventory.quantity = final_quantity

    mod = Modification(slot_id=None, item_id=int_id, source=ModSource.MAIN_INVENTORY, mod_type=ModType.RESTOCK, quantity_start=start_quantity, quantity_final=final_quantity, threshold=item.main_inventory.low_stock_threshold)

    session.add(mod)
    session.flush()
    return item

def modify_stock(session: Session, id: str, quantity: str) -> MainInventory:
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
    check.check_item_main_inventory(item, int_id, errors_id)
    if errors_id:
        errors["id"] = errors_id
        raise ValueError(errors)
    
    start_quantity = item.main_inventory.quantity
    item.main_inventory.quantity = int_quantity

    mod = Modification(slot_id=None, item_id=int_id, source=ModSource.MAIN_INVENTORY, mod_type=ModType.MANUAL, quantity_start=start_quantity, quantity_final=int_quantity, threshold=item.main_inventory.low_stock_threshold)
    
    session.add(mod)
    session.flush()
    return item

def modify_threshold(session: Session, id: str, threshold: str) -> MainInventory:
    errors = {}
    errors_id = []
    errors_threshold = []

    strip_id = id.strip()
    strip_threshold = threshold.strip()

    check.check_id_nop(strip_id, errors_id)
    check.check_threshold_nop(strip_threshold, errors_threshold)

    for field, field_errors in (("id", errors_id), ("threshold", errors_threshold)):
        if field_errors:
            errors[field] = field_errors

    if errors:
        raise ValueError(errors)
    
    int_id = int(strip_id)
    int_threshold = int(strip_threshold)

    item = session.get(Item, int_id)
    check.check_item_main_inventory(item, int_id, errors_id)
    if errors_id:
        errors["id"] = errors_id
        raise ValueError(errors)
    
    item.main_inventory.low_stock_threshold = int_threshold

    mod = Modification(slot_id=None, item_id=int_id, source=ModSource.MAIN_INVENTORY, mod_type=ModType.MANUAL, quantity_start=item.main_inventory.quantity, quantity_final=item.main_invetory.quantity, threshold=int_threshold)

    session.add(mod)
    session.flush()
    return item

def check_low_stock(session: Session) -> list[dict]:
    low_stock_items = list_low_stock(session)
    return [
        {
            "id": low_stock_item.item_id,
            "name": low_stock_item.item.name,
            "quantity": low_stock_item.quantity,
            "threshold": low_stock_item.low_stock_threshold
        }
        for low_stock_item in low_stock_items
    ]