from sqlalchemy.orm import Session
from decimal import Decimal

from tables.transaction import Transaction
from utilities.error_checking import ErrorChecking as ec

def record_transaction(session: Session, item_price: str, amount: str) -> Transaction:
    errors = {}
    errors_price = []
    errors_amount = []
    
    price_stripped = item_price.strip()
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
    
    transaction = Transaction(item_price=dec_price, amount=int_amount)
    
    session.add(transaction)
    session.flush()
    
    return transaction