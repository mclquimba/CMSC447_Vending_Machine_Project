from typing import Optional
from decimal import Decimal, InvalidOperation

from tables.vm_slot import MAX_NAME_CHARS, MAX_SLOT_CHARS, DEFAULT_CUR_QUANTITY, DEFAULT_MAX_QUANTITY, DEFAULT_THRESHOLD
from tables.user import MAX_USERNAME_CHARS, Role
from seed import SLOT_VALUES

class ErrorChecking:
    # Not Optional
    @staticmethod
    def check_name_nop(name: str, errors_name: list[str]) -> int:
        name_stripped = name.strip()
        num_errors = 0
        
        if not name_stripped:
            errors_name.append("Name field can not be empty.")
            num_errors += 1
        else:
            if len(name_stripped) > MAX_NAME_CHARS:
                errors_name.append(f"Name field can not exceed {MAX_NAME_CHARS} characters.")
                num_errors += 1
            
        return num_errors
    
    @staticmethod
    def check_price_nop(price: str, errors_price: list[str]) -> int:
        price_stripped = price.strip()
        num_errors = 0
        
        if not price_stripped:
            errors_price.append("Price field can not be empty.")
            num_errors += 1
        else:
            try:
                dec_price = Decimal(price_stripped)
                
                if dec_price < 0:
                    errors_price.append("Price can not be negative.")
                    num_errors += 1
                    
                exponent = dec_price.as_tuple().exponent
                if isinstance(exponent, int) and exponent < -2:
                    errors_price.append("Price must be in the format #.##.")
                    num_errors += 1
            except InvalidOperation:
                errors_price.append("Price must be in the format #.##.")
                num_errors += 1
        
        return num_errors
    
    @staticmethod
    def check_slot_nop(slot: str, errors_slot: list[str]) -> int:
        slot_stripped = slot.strip().upper()
        num_errors = 0
        
        if not slot_stripped:
            errors_slot.append("Slot field can not be empty.")
            num_errors += 1
        elif slot_stripped not in SLOT_VALUES:
            errors_slot.append(f"{slot_stripped} not in {", ".join(SLOT_VALUES)}.")
            num_errors += 1
        
        return num_errors
    
    @staticmethod
    def check_quantity_cur_nop(quantity_cur: str, errors_quantity_cur: list[str]) -> int:
        quantity_cur_stripped = quantity_cur.strip()
        num_errors = 0
        
        if not quantity_cur_stripped:
            errors_quantity_cur.append("Current Quantity field can not be empty.")
            num_errors += 1
        else:
            try:
                int_quantity_cur = int(quantity_cur_stripped)
                if int_quantity_cur < 0:
                    errors_quantity_cur.append("Current Quantity can not be negative.")
                    num_errors += 1
            except ValueError:
                errors_quantity_cur.append("Current Quantity must be an integer.")
                num_errors += 1
        
        return num_errors
    
    @staticmethod
    def check_threshold_nop(threshold: str, errors_threshold: list[str]) -> int:
        threshold_stripped = threshold.strip()
        num_errors = 0
        
        if not threshold_stripped:
            errors_threshold.append("Threshold field can not be empty.")
            num_errors += 1
        else:
            try:
                int_threshold = int(threshold_stripped)
                if int_threshold <= 0:
                    errors_threshold.append("Threshold must be greater than 0.")
                    num_errors += 1
                if int_threshold >= DEFAULT_MAX_QUANTITY:
                    errors_threshold.append(f"Threshold must be smaller than max quantity: {DEFAULT_MAX_QUANTITY}")
                    num_errors += 1
            except ValueError:
                errors_threshold.append("Threshold must be an integer.")
                num_errors += 1
        
        return num_errors
    
    @staticmethod
    def check_amount_nop(amount: str, errors_amount: list[str]) -> int:
        amount_stripped = amount.strip()
        num_errors = 0
        
        if not amount_stripped:
            errors_amount.append("Quantity field can not be empty.")
            num_errors += 1
        else:
            try:
                int_amount = int(amount_stripped)
                if int_amount <= 0:
                    errors_amount.append("Quantity must be greater than 0.")
                    num_errors += 1
            except ValueError:
                errors_amount.append("Quantity must be an integer.")
                num_errors += 1
        
        return num_errors
    
    @staticmethod
    def check_username_nop(username: str, errors_username: list[str]) -> int:
        num_errors = 0
        if len(username) > MAX_USERNAME_CHARS:
            errors_username.append(f"Username field can not exceed {MAX_USERNAME_CHARS} characters.")
            num_errors += 1
        return num_errors
    
    @staticmethod
    def check_user_id_nop(user_id: str, errors_user_id: list[str]) -> int:
        user_id_stripped = user_id.strip()
        num_errors = 0
        
        try:
            int_user_id = int(user_id_stripped)
            if int_user_id <= 0:
                errors_user_id.append("User ID must be greater than 0.")
                num_errors += 1
        except ValueError:
            errors_user_id.append("User ID must be an integer.")
            num_errors += 1
            
        return num_errors
    
    # Optional
    @staticmethod
    def check_name_op(name: str, errors_name: list[str]) -> int:
        name_stripped = name.strip()
        num_errors = 0
        
        if name_stripped:
            if len(name_stripped) > MAX_NAME_CHARS:
                errors_name.append(f"Name field can not exceed {MAX_NAME_CHARS} characters.")
                num_errors += 1
        
        return num_errors
        
    @staticmethod
    def check_price_op(price: str, errors_price: list[str]) -> int:
        price_stripped = price.strip()
        num_errors = 0
        
        if price_stripped:
            try:
                dec_price = Decimal(price_stripped)
                if dec_price < 0:
                    errors_price.append("Price can not be negative.")
                    num_errors += 1
                
                exponent = dec_price.as_tuple().exponent
                if isinstance(exponent, int) and exponent < -2:
                    errors_price.append("Price must be in the format #.##.")
                    num_errors += 1
            except InvalidOperation:
                errors_price.append("Price must be in the format #.##.")
                num_errors += 1
                
        return num_errors
    
    @staticmethod
    def check_quantity_cur_op(quantity_cur: str, errors_quantity_cur: list[str]) -> int:
        quantity_cur_stripped = quantity_cur.strip()
        num_errors = 0
        
        if quantity_cur_stripped:
            try:
                int_quantity_cur = int(quantity_cur_stripped)
                if int_quantity_cur < 0:
                    errors_quantity_cur.append("Current Quantity can not be negative.")
                    num_errors += 1
            except ValueError:
                errors_quantity_cur.append("Current Quantity must be an integer.")
                num_errors += 1
        
        return num_errors
        
    @staticmethod
    def check_threshold_op(threshold: str, errors_threshold: list[str]) -> int:
        threshold_stripped = threshold.strip()
        num_errors = 0
        
        if threshold_stripped:
            try:
                int_threshold = int(threshold_stripped)
                if int_threshold <= 0:
                    errors_threshold.append("Threshold must be greater than 0.")
                    num_errors += 1
            except ValueError:
                errors_threshold.append("Threshold must be an integer.")
                num_errors += 1
                
        return num_errors