from sqlalchemy import select, case
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import Optional

from tables.vm_slot import VendingMachineSlot, Status
import logic.modification_logic as mod

from utilities.error_checking import ErrorChecking as ec

def get_slot(session: Session, slot_value: str, errors_slot: list[str]) -> Optional[VendingMachineSlot]:
    slot_stripped = slot_value.strip().upper()
    query = select(VendingMachineSlot).where(VendingMachineSlot.slot_value == slot_stripped)
    slot = session.scalars(query).first()
    if slot is None:
        errors_slot.append(f"Slot {slot_stripped} is not initialized.")
    return slot

def get_purchase(session: Session, price: Decimal, errors_price: list[str]) -> Optional[VendingMachineSlot]:
    query = select(VendingMachineSlot).where(VendingMachineSlot.item_price == price)
    slot = session.scalars(query).first()
    if slot is None:
        errors_price.append(f"No item with price ${price}.")
    return slot

def get_status(quantity_cur: int, threshold: int) -> Status:
    if quantity_cur == 0:
        return Status.OUT
    elif quantity_cur <= threshold:
        return Status.LOW
    return Status.GOOD

# if item_name is None, make sure item_price is None & make quantity_cur 0
# if item_price is None, make sure item_name is None & make quantity_cur 0
# if price is not None, if price exists in database, make sure slot_value is the same as database slot_value
def manual(session: Session, slot_value: str, item_name: str, item_price: str, quantity_cur: str, threshold: str) -> VendingMachineSlot:
    errors = {}
    errors_slot = []
    errors_name = []
    errors_price = []
    errors_quantity_cur = []
    errors_threshold = []
    
    slot_stripped = slot_value.strip().upper()
    name_stripped = item_name.strip()
    price_stripped = item_price.strip()
    quantity_cur_stripped = quantity_cur.strip()
    threshold_stripped = threshold.strip()
        
    ec.check_slot_nop(slot_stripped, errors_slot)
    ec.check_name_op(name_stripped, errors_name)
    ec.check_price_op(price_stripped, errors_price)
    ec.check_quantity_cur_nop(quantity_cur_stripped, errors_quantity_cur)
    ec.check_threshold_nop(threshold_stripped, errors_threshold)
    
    for field, field_errors in (("slot", errors_slot), ("name", errors_name), ("price", errors_price), ("current_quantity", errors_quantity_cur), ("threshold", errors_threshold)):
        if field_errors:
            errors[field] = field_errors
            
    if errors:
        raise ValueError(errors)
    
    int_quantity_cur = int(quantity_cur_stripped)
    int_threshold = int(threshold_stripped)
    
    if not name_stripped:
        name_stripped = None
        
    if not price_stripped:
        dec_price = None
    else:
        dec_price = Decimal(price_stripped)

    # Make a check (if item_name is null, item_price must be null) (if item_price is null, item_name must be null)
    if name_stripped is None:
        if dec_price is not None:
            errors_price.append("Name field is empty but price field is not empty.")
            errors["price"] = errors_price
            raise ValueError(errors)
        else:
            int_quantity_cur = 0
            
    if dec_price is None:
        if name_stripped is not None:
            errors_name.append("Price field is empty but name field is not empty.")
            errors["name"] = errors_name
            raise ValueError(errors)
        else:
            int_quantity_cur = 0
    
    slot = get_slot(session, slot_stripped, errors_slot)
    if slot is None:
        errors["slot"] = errors_slot
        raise ValueError(errors)
    
    if dec_price is not None:
        query = select(VendingMachineSlot).where(VendingMachineSlot.item_price == dec_price)
        existing_slot = session.scalars(query).first()
        if existing_slot:
            if existing_slot.slot_value != slot.slot_value:
                errors_price.append(f"Price ${dec_price} exists in the Vending Machine.")
                errors["price"] = errors_price
                raise ValueError(errors)
    
    status = get_status(int_quantity_cur, int_threshold)
    
    mod._mod_manual(session, slot=slot, new_item_name=name_stripped, new_item_price=dec_price, new_quantity_cur=int_quantity_cur, new_threshold=int_threshold)
    
    slot.item_name = name_stripped
    slot.item_price = dec_price
    slot.quantity_cur = int_quantity_cur
    slot.threshold = int_threshold
    slot.status = status
    
    session.flush()
    return slot

def clear_slot(session: Session, slot_value: str) -> VendingMachineSlot:
    errors = {}
    errors_slot = []
    
    slot_stripped = slot_value.strip().upper()
    
    ec.check_slot_nop(slot_stripped, errors_slot)
    
    for field, field_errors in [("slot", errors_slot)]:
        if field_errors:
            errors[field] = field_errors
            
    if errors:
        raise ValueError(errors)
    
    slot = get_slot(session, slot_stripped, errors_slot)
    if slot is None:
        errors["slot"] = errors_slot
        raise ValueError(errors)
    
    mod._mod_manual(session, slot=slot, new_item_name=None, new_item_price=None, new_quantity_cur=0, new_threshold=slot.threshold)
    
    slot.item_name = None
    slot.item_price = None
    slot.quantity_cur = 0
    slot.status = Status.OUT
    
    session.flush()
    return slot
    
def restock(session: Session, slot_value: str, amount: str) -> VendingMachineSlot:
    errors = {}
    errors_slot = []
    errors_amount = []
    
    slot_stripped = slot_value.strip().upper()
    amount_stripped = amount.strip()
    
    ec.check_slot_nop(slot_stripped, errors_slot)
    ec.check_amount_nop(amount_stripped, errors_amount)
    
    for field, field_errors in (("slot", errors_slot), ("amount", errors_amount)):
        if field_errors:
            errors[field] = field_errors
            
    if errors:
        raise ValueError(errors)
    
    int_amount = int(amount_stripped)
    
    slot = get_slot(session, slot_stripped, errors_slot)
    if slot is None:
        errors["slot"] = errors_slot
        raise ValueError(errors)
    
    quantity_cur = slot.quantity_cur
    quantity_max = slot.quantity_max
    quantity_total = quantity_cur + int_amount
    cap_remaining = quantity_max - quantity_cur
    
    if quantity_total > quantity_max:
        errors_amount.append(f"Added amount exceeds remaining capacity. Remaining Capacity: {cap_remaining}.")
        errors["amount"] = errors_amount
        raise ValueError(errors)
    
    status = get_status(quantity_total, slot.threshold)
    
    mod._mod_restock(session, slot, quantity_total)
    
    slot.quantity_cur = quantity_total
    slot.status = status
    
    session.flush()
    return slot
    
def purchase(session: Session, price: str, amount: str) -> VendingMachineSlot:
    errors = {}
    errors_price = []
    errors_amount = []
    
    price_stripped = price.strip()
    amount_stripped = amount.strip()
    
    ec.check_price_nop(price_stripped, errors_price)
    ec.check_amount_nop(amount_stripped, errors_amount)
    
    for field, field_errors in (("price", errors_price), ("amount", errors_amount)):
        if field_errors:
            errors[field] = field_errors
            
    if errors:
        raise ValueError(errors)
    
    int_amount = int(amount_stripped)
    dec_price = Decimal(price_stripped)
    
    slot = get_purchase(session, dec_price, errors_price)
    if slot is None:
        errors["price"] = errors_price
        raise ValueError(errors)

    quantity_cur = slot.quantity_cur
    
    if int_amount > quantity_cur:
        errors_amount.append(f"Purchase amount exceeds current quantity. Current Quantity: {quantity_cur}.")
        errors["amount"] = errors_amount
        raise ValueError(errors)
    
    new_quantity = quantity_cur - int_amount
    
    status = get_status(new_quantity, slot.threshold)
    
    mod._mod_transaction(session, slot=slot, new_quantity_cur=new_quantity)
    
    slot.quantity_cur = new_quantity
    slot.status = status
    
    session.flush()
    return slot
        
def list_stock_slot(session: Session) -> list[VendingMachineSlot]:
    query = select(VendingMachineSlot).order_by(VendingMachineSlot.slot_value)
    return list(session.scalars(query).all())
    
def list_stock_status(session: Session) -> list[VendingMachineSlot]:  
    status = case(
        (VendingMachineSlot.status == Status.OUT, 0),
        (VendingMachineSlot.status == Status.LOW, 1),
        (VendingMachineSlot.status == Status.GOOD, 2)
    )
    
    query = select(VendingMachineSlot).where(VendingMachineSlot.item_name.is_not(None)).order_by(status, VendingMachineSlot.slot_value)
    
    return list(session.scalars(query).all())