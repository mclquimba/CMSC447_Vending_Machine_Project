from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from classes.item import Item, MAX_NAME, MAX_CAT
from utilities.error_checking import ErrorChecking as check
from decimal import Decimal

def create_item(session: Session, name: str, price: str, category: str) -> Item:
    errors = {}
    errors_name = []
    errors_price = []
    errors_category = []

    strip_name = name.strip()
    strip_category = category.strip()
    strip_price = price.strip()

    check.check_name_nop(strip_name, errors_name)
    check.check_price_nop(strip_price, errors_price)
    check.check_category_nop(strip_category, errors_category)

    for field, field_errors in (("name", errors_name), ("price", errors_price), ("category", errors_category)):
        if field_errors:
            errors[field] = field_errors
    
    if errors:
        raise ValueError(errors)
    
    dec_price = Decimal(strip_price)

    item = Item(name=strip_name, price=dec_price, category=strip_category)
    session.add(item)
    session.flush()
    return item

def get_item(session: Session, id: str) -> Item:
    errors = {}
    errors_id = []

    strip_id = id.strip()

    check.check_id_nop(strip_id, errors_id)

    if errors_id:
        errors["id"] = errors_id
        raise ValueError(errors)
    
    int_id = int(strip_id)
    
    item = session.get(Item, int_id)
    if item is None:
        raise ValueError({"id": [f"Item {int_id} not found."]})
    
    return item

def search_items(session: Session, string: str) -> list[Item]:
    query = select(Item).order_by(Item.name)
    if string:
        to_search = f"%{string.strip().lower()}%"
        query = query.where(Item.name.ilike(to_search))
    return list(session.scalars(query))

def modify_item(session: Session, id: str, name: str, price: str, category: str) -> Item:
    errors = {}
    errors_name = []
    errors_id = []
    errors_price = []
    errors_category = []

    strip_id = id.strip()
    strip_price = price.strip()
    strip_name = name.strip()
    strip_category = category.strip()

    check.check_id_nop(strip_id, errors_id)
    check.check_name_op(strip_name, errors_name)
    check.check_price_op(strip_price, errors_price)
    check.check_category_op(strip_category, errors_category)

    for field, field_errors in (("id", errors_id), ("price", errors_price), ("name", errors_name), ("category", errors_category)):
        if field_errors:
            errors[field] = field_errors
        
    if errors:
        raise ValueError(errors)
    
    int_id = int(strip_id)
    dec_price = Decimal(strip_price)

    item = session.get(Item, int_id)
    if item is None:
        raise ValueError({"id": [f"Item {int_id} not found."]})
    
    if strip_name:
        item.name = strip_name
    if strip_price:
        item.price = dec_price
    if strip_category:
        item.category = strip_category
    
    session.flush()
    return item

def delete_item(session:Session, id: str) -> dict:
    errors = {}
    errors_id = []

    strip_id = id.strip()

    check.check_id_nop(strip_id, errors_id)

    if errors_id:
        errors["id"] = errors_id
        raise ValueError(errors)
    
    int_id = int(strip_id)

    item = session.get(Item, int_id)
    if item is None:
        raise ValueError({"id": [f"Item {int_id} not found."]})
    
    vending_machine_slots = [slot.slot_value for slot in item.vending_machine_slots]
    item_info = {
        "id": item.id,
        "name": item.name,
        "slot_values": vending_machine_slots
    }

    session.delete(item)
    session.flush()

    return item_info