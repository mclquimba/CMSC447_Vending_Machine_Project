from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal

from tables.modification import Modification, ModType
from tables.vm_slot import VendingMachineSlot

def _mod_manual(session: Session, slot: VendingMachineSlot, new_item_name: Optional[str], new_item_price: Optional[Decimal], new_quantity_cur: int, new_threshold: int) -> bool:
    if slot is None:
        return False
    
    item_name_old = slot.item_name
    item_price_old = slot.item_price
    quantity_cur_old = slot.quantity_cur
    threshold_old = slot.threshold
    
    item_name_new = new_item_name
    item_price_new = new_item_price
    quantity_cur_new = new_quantity_cur
    threshold_new = new_threshold
    
    mod = Modification(type=ModType.MANUAL,
                       old_item_name=item_name_old,
                       new_item_name=item_name_new,
                       old_item_price=item_price_old,
                       new_item_price=item_price_new,
                       old_quantity_cur=quantity_cur_old,
                       new_quantity_cur=quantity_cur_new,
                       old_threshold=threshold_old,
                       new_threshold=threshold_new)
    
    session.add(mod)
    session.flush()
    
    return True

def _mod_restock(session: Session, slot: VendingMachineSlot, new_quantity_cur: int) -> bool:
    if slot is None:
        return False
    
    item_name_old = slot.item_name
    item_price_old = slot.item_price
    quantity_cur_old = slot.quantity_cur
    threshold_old = slot.threshold
    
    item_name_new = slot.item_name
    item_price_new = slot.item_price
    quantity_cur_new = new_quantity_cur
    threshold_new = slot.threshold
    
    mod = Modification(type=ModType.RESTOCK,
                       old_item_name=item_name_old,
                       new_item_name=item_name_new,
                       old_item_price=item_price_old,
                       new_item_price=item_price_new,
                       old_quantity_cur=quantity_cur_old,
                       new_quantity_cur=quantity_cur_new,
                       old_threshold=threshold_old,
                       new_threshold=threshold_new)
    
    session.add(mod)
    session.flush()
    
    return True

def _mod_transaction(session: Session, slot: VendingMachineSlot, new_quantity_cur: int) -> bool:
    if slot is None:
        return False
    
    item_name_old = slot.item_name
    item_price_old = slot.item_price
    quantity_cur_old = slot.quantity_cur
    threshold_old = slot.threshold
    
    item_name_new = slot.item_name
    item_price_new = slot.item_price
    quantity_cur_new = new_quantity_cur
    threshold_new = slot.threshold
    
    mod = Modification(type=ModType.TRANSACTION,
                       old_item_name=item_name_old,
                       new_item_name=item_name_new,
                       old_item_price=item_price_old,
                       new_item_price=item_price_new,
                       old_quantity_cur=quantity_cur_old,
                       new_quantity_cur=quantity_cur_new,
                       old_threshold=threshold_old,
                       new_threshold=threshold_new)
    
    session.add(mod)
    session.flush()
    
    return True