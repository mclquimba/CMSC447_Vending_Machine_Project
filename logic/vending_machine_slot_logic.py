from sqlalchemy import select
from sqlalchemy.orm import Session

from typing import List
from utilities.error_checking import ErrorChecking as check
from classes.main_inventory import MainInventory
from classes.vending_machine_slot import VendingMachineSlot
from classes.item import Item
from classes.inventory_modifications import Modification, ModSource, ModType

def assign_slot(session: Session, item_id: str, slot_value: str, quantity: str, threshold: str) -> VendingMachineSlot:
    errors = {}
    errors_id = []
    errors_value = []
    errors_quantity = []
    errors_threshold = []
    
    strip_id = item_id.strip()
    strip_value = slot_value.strip()
    strip_quantity = quantity.strip()
    strip_threshold = threshold.strip()
    
    check.check_id_nop(strip_id, errors_id)
    check.check_slot_value_nop(strip_value, errors_value)
    check.check_quantity_nop(strip_quantity, errors_quantity)
    check.check_threshold_nop(strip_threshold, errors_threshold)
    
    for field, field_errors in (("id", errors_id), ("slot_value", errors_value), ("quantity", errors_quantity), ("threshold", errors_threshold)):
        if field_errors:
            errors[field] = field_errors
            
    if errors:
        raise ValueError(errors)
    
    int_id = int(strip_id)
    int_quantity = int(strip_quantity)
    int_threshold = int(strip_threshold)

    new_item = session.get(Item, int_id)
    check.check_item_main_inventory(new_item, int_id, errors_id)
    if errors_id:
        errors["id"] = errors_id
        raise ValueError(errors)
    if new_item.main_inventory.quantity < int_quantity:
        errors_id.append(f"Not enough stock for Item {int_id}. {new_item.main_inventory.quantity} left.")
        errors["id"] = errors_id
        raise ValueError(errors)
    
    slot = get_slot(session, strip_value, errors_value)
    if errors_value:
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    if int_quantity > slot.cap:
        errors_quantity.append(f"Not enough space in the slot. {slot.cap} left.")
        errors["quantity"] = errors_quantity
        raise ValueError(errors)
    
    if slot.item_id is not None:
        old_item = session.get(Item, slot.item_id)

        start_quantity = old_item.main_inventory.quantity
        final_quantity = start_quantity + slot.quantity
        old_item.main_inventory.quantity = final_quantity

        old_to_main_inventory = Modification(slot_id=None, item_id=slot.item_id, source=ModSource.MAIN_INVENTORY, mod_type=ModType.MANUAL, quantity_start=start_quantity, quantity_final=final_quantity, threshold=old_item.main_inventory.low_stock_threshold)
        session.add(old_to_main_inventory)

        reset_vending_machine_slot = Modification(slot_id=slot.id, item_id=slot.item_id, source=ModSource.VM_SLOT, mod_type=ModType.MANUAL, quantity_start=slot.quantity, quantity_final=0, threshold=slot.low_stock_threshold)
        session.add(reset_vending_machine_slot)

    start_quantity = new_item.main_inventory.quantity
    final_quantity = start_quantity - int_quantity
    new_item.main_inventory.quantity = final_quantity

    slot.item_id = int_id
    slot.quantity = int_quantity
    slot.low_stock_threshold = int_threshold

    new_to_vending_machine_slot = Modification(slot_id=slot.id, item_id=int_id, source=ModSource.VM_SLOT, mod_type=ModType.MANUAL, quantity_start=0, quantity_final=int_quantity, threshold=int_threshold)
    session.add(new_to_vending_machine_slot)

    modify_main_inventory_item = Modification(slot_id=None, item_id=int_id, source=ModSource.MAIN_INVENTORY, mod_type=ModType.MANUAL, quantity_start=start_quantity, quantity_final=final_quantity, threshold=new_item.main_inventory.low_stock_threshold)
    session.add(modify_main_inventory_item)

    session.flush()
    return slot
    
def get_slot(session:Session, slot_value: str, errors_value: List[str]) -> VendingMachineSlot:
    strip_value = slot_value.strip().upper()
    query = select(VendingMachineSlot).where(VendingMachineSlot.slot_value == strip_value)
    slot = session.scalar(query)
    if slot is None:
        errors_value.append(f"Slot {strip_value} is not initialized.")
    return slot

def unassign_slot(session: Session, slot_value: str) -> VendingMachineSlot:
    errors = {}
    errors_value = []
    errors_id = []

    strip_value = slot_value.strip()

    check.check_slot_value_nop(strip_value, errors_value)
    if errors_value:
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    
    slot = get_slot(session, strip_value, errors_value)
    if errors_value:
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    if slot.item_id is None:
        errors_value.append(f"Slot {strip_value} is already empty.")
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    
    item = session.get(Item, slot.item_id)
    check.check_item_main_inventory(item, item.id, errors_id)
    if errors_id:
        errors["id"] = errors_id
        raise ValueError(errors)
    
    start_quantity = item.main_inventory.quantity
    final_quantity = start_quantity + slot.quantity
    item.main_inventory.quantity = final_quantity

    cur_slot_quantity = slot.quantity
    slot.item_id = None
    slot.quantity = 0
    
    item_to_main_inventory = Modification(slot_id=None, item_id=item.id, source=ModSource.MAIN_INVENTORY, mod_type=ModType.MANUAL, quantity_start=start_quantity, quantity_final=final_quantity, threshold=item.main_inventory.low_stock_threshold)
    session.add(item_to_main_inventory)

    reset_vending_machine_slot = Modification(slot_id=slot.id, item_id=item.id, source=ModSource.VM_SLOT, mod_type=ModType.MANUAL, quantity_start=cur_slot_quantity, quantity_final=0, threshold=slot.low_stock_threshold)
    session.add(reset_vending_machine_slot)

    session.flush()
    return slot

def restock_slot(session: Session, slot_value: str, change: str) -> VendingMachineSlot:
    errors = {}
    errors_value = []
    errors_change = []
    errors_id = []

    strip_value = slot_value.strip()
    strip_change = change.strip()

    check.check_slot_value_nop(strip_value, errors_value)
    check.check_quantity_nop(strip_change, errors_change)

    for field, field_errors in (("slot_value", errors_value), ("quantity", errors_change)):
        if field_errors:
            errors[field] = field_errors

    if errors:
        raise ValueError(errors)
    
    int_change = int(strip_change)

    slot = get_slot(session, strip_value, errors_value)
    if errors_value:
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    if slot.item_id is None:
        errors_value.append(f"Slot {strip_value} is empty.")
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    
    item = session.get(Item, slot.item_id)
    check.check_item_main_inventory(item, item.id, errors_id)
    if errors_id:
        errors["id"] = errors_id
        raise ValueError(errors)
    
    if item.main_inventory.quantity < int_change:
        errors_change.append(f"Not enough stock for items in Slot {slot.slot_value}. {item.main_inventory.quantity} left.")
        errors["change"] = errors_change
        raise ValueError(errors)
    
    available = slot.cap - slot.quantity
    if int_change > available:
        errors_change.append(f"Not enough space in the slot. {available} available.")
        errors["quantity"] = errors_change
        raise ValueError(errors)
    
    start_quantity_main = item.main_inventory.quantity
    final_quantity_main = start_quantity_main - int_change
    start_quantity_slot = slot.quantity
    final_quantity_slot = start_quantity_slot + int_change

    item.main_inventory.quantity = final_quantity_main
    slot.quantity = final_quantity_slot

    mod_inventory = Modification(slot_id=None, item_id=item.id, source=ModSource.MAIN_INVENTORY, mod_type=ModType.RESTOCK, quantity_start=start_quantity_main, quantity_final=final_quantity_main, threshold=item.main_inventory.low_stock_threshold)
    session.add(mod_inventory)

    mod_vending_machine = Modification(slot_id=slot.id, item_id=item.id, source=ModSource.VM_SLOT, mod_type=ModType.RESTOCK, quantity_start=start_quantity_slot, quantity_final=final_quantity_slot, threshold=slot.low_stock_threshold)
    session.add(mod_vending_machine)

    session.flush()
    return slot

def modify_slot_stock(session: Session, slot_value: str, quantity: str) -> VendingMachineSlot:
    errors = {}
    errors_value = []
    errors_quantity = []
    errors_id = []

    strip_value = slot_value.strip()
    strip_quantity = quantity.strip()

    check.check_slot_value_nop(strip_value, errors_value)
    check.check_quantity_nop(strip_quantity, errors_quantity)

    for field, field_errors in (("slot_value", errors_value), ("quantity", errors_quantity)):
        if field_errors:
            errors[field] = field_errors

    if errors:
        raise ValueError(errors)

    int_quantity = int(strip_quantity)

    slot = get_slot(session, strip_value, errors_value)
    if errors_value:
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    if int_quantity > slot.cap:
        errors_quantity.append(f"Not enough space in the slot. {slot.cap} is maximum capacity.")
        errors["quantity"] = errors_quantity
        raise ValueError(errors)
    if slot.item_id is None:
        errors_value.append(f"Slot {strip_value} is empty.")
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    
    item = session.get(Item, slot.item_id)
    check.check_item_main_inventory(item, item.id, errors_id)
    if errors_id:
        errors["id"] = errors_id
        raise ValueError(errors)
    total_stock = item.main_inventory.quantity + slot.quantity
    if int_quantity > total_stock:
        errors_quantity.append(f"Not enough stock. {total_stock} available.")
        errors["quantity"] = errors_quantity
        raise ValueError(errors)
    
    start_quantity_main = item.main_inventory.quantity
    final_quantity_main = total_stock - int_quantity

    start_quantity_slot = slot.quantity
    final_quantity_slot = int_quantity

    item.main_inventory.quantity = final_quantity_main
    slot.quantity = final_quantity_slot

    mod_inventory = Modification(slot_id=None, item_id=item.id, source=ModSource.MAIN_INVENTORY, mod_type=ModType.MANUAL, quantity_start=start_quantity_main, quantity_final=final_quantity_main, threshold=item.main_inventory.low_stock_threshold)
    session.add(mod_inventory)

    mod_vending_machine = Modification(slot_id=slot.id, item_id=item.id, source=ModSource.VM_SLOT, mod_type=ModType.MANUAL, quantity_start= start_quantity_slot, quantity_final=final_quantity_slot, threshold=slot.low_stock_threshold)
    session.add(mod_vending_machine)

    session.flush()
    return slot

def modify_threshold(session: Session, slot_value: str, threshold: str) -> VendingMachineSlot:
    errors = {}
    errors_value = []
    errors_threshold = []

    strip_value = slot_value.strip()
    strip_threshold = threshold.strip()

    check.check_slot_value_nop(strip_value, errors_value)
    check.check_threshold_nop(strip_threshold, errors_threshold)

    for field, field_errors in (("slot_value", errors_value), ("threshold", errors_threshold)):
        if field_errors:
            errors[field] = field_errors

    if errors:
        raise ValueError(errors)
    
    int_threshold = int(strip_threshold)

    slot = get_slot(session, strip_value, errors_value)
    if errors_value:
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    if slot.item_id is None:
        errors_value.append(f"Slot {strip_value} is empty.")
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    
    slot.low_stock_threshold = int_threshold

    mod = Modification(slot_id=slot.id, item_id=slot.item_id, source=ModSource.VM_SLOT, mod_type=ModType.MANUAL, quantity_start=slot.quantity, quantity_final=slot.quantity, threshold=int_threshold)
    session.add(mod)

    session.flush()
    return slot
    
def transaction(session: Session, slot_value: str, quantity: str) -> VendingMachineSlot:
    errors = {}
    errors_value = []
    errors_quantity = []

    strip_value = slot_value.strip()
    strip_quantity = quantity.strip()

    check.check_slot_value_nop(strip_value, errors_value)
    check.check_quantity_nop(strip_quantity, errors_quantity)

    for field, field_errors in (("slot_value", errors_value), ("quantity", errors_quantity)):
        if field_errors:
            errors[field] = field_errors

    if errors:
        raise ValueError(errors)
    
    int_quantity = int(strip_quantity)

    slot = get_slot(session, strip_value, errors_value)
    if errors_value:
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    if slot.item_id is None:
        errors_value.append(f"Slot {strip_value} is empty.")
        errors["slot_value"] = errors_value
        raise ValueError(errors)
    
    if int_quantity > slot.quantity:
        errors_quantity.append(f"Not enough stock. {slot.quantity} available.")
        errors["quantity"] = errors_quantity
        raise ValueError(errors)
    
    start_quantity = slot.quantity
    final_quantity = slot.quantity - int_quantity
    slot.quantity = final_quantity

    mod = Modification(slot_id=slot.id, item_id=slot.item_id, source=ModSource.VM_SLOT, mod_type=ModType.TRANSACTION, quantity_start=start_quantity, quantity_final=final_quantity, threshold=slot.low_stock_threshold)
    session.add(mod)

    session.flush()
    return slot
    
def list_low_slots(session: Session) -> list[VendingMachineSlot]:
    query = select(VendingMachineSlot).order_by(VendingMachineSlot.slot_value).where(VendingMachineSlot.quantity < VendingMachineSlot.low_stock_threshold)
    return list(session.scalars(query))

def list_slots(session: Session) -> list[VendingMachineSlot]:
    query = select(VendingMachineSlot).order_by(VendingMachineSlot.slot_value)
    return list(session.scalars(query))

def check_low_stock(session: Session) -> list[dict]:
    low_stock_slots = list_low_slots(session)

    final_low_stock_slots = []

    for low_stock_slot in low_stock_slots:
        if low_stock_slot.item_id is not None:
            final_low_stock_slots.append(
                {
                    "slot_value": low_stock_slot.slot_value,
                    "id": low_stock_slot.item_id,
                    "name": low_stock_slot.item.name,
                    "quantity": low_stock_slot.quantity,
                    "threshold": low_stock_slot.low_stock_threshold
                }
            )

    return final_low_stock_slots