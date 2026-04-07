from typing import List, Optional
from decimal import Decimal, InvalidOperation

from classes.item import Item, MAX_NAME, MAX_CAT
from seed import SLOT_VALUES

class ErrorChecking:
    # Currently built:
    # id_nop, name_nop, price_nop, category_nop, quantity_nop
    # name_op, price_op, category_op

    # Not Optional
    @staticmethod
    def check_id_nop(id: str, errors_id: List[str]) -> int:
        strip_id = id.strip()
        num_errors = 0

        if not strip_id:
            errors_id.append("ID field can not be empty.")
            num_errors += 1
        else:
            try:
                int_id = int(strip_id)
                if int_id <= 0:
                    errors_id.append("ID must be greater than 0.")
                    num_errors += 1
            except ValueError:
                errors_id.append("ID must be an integer.")
                num_errors += 1
            
        return num_errors
    
    @staticmethod
    def check_name_nop(name: str, errors_name: List[str]) -> int:
        strip_name = name.strip()
        num_errors = 0

        if not strip_name:
            errors_name.append("Name field can not be empty.")
            num_errors += 1
        else:
            if len(strip_name) > MAX_NAME:
                errors_name.append(f"Name field can not exceed {MAX_NAME} characters.")
                num_errors += 1
        
        return num_errors
    
    @staticmethod
    def check_price_nop(price: str, errors_price: List[str]) -> int:
        strip_price = price.strip()
        num_errors = 0

        if not strip_price:
            errors_price.append("Price field can not be empty.")
            num_errors += 1
        else:
            try:
                dec_price = Decimal(strip_price)

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
    def check_category_nop(category: str, errors_category: List[str]) -> int:
        strip_category = category.strip()
        num_errors = 0

        if not strip_category:
            errors_category.append("Category field can not be empty.")
            num_errors += 1
        else:
            if len(strip_category) > MAX_CAT:
                errors_category.append(f"Category field can not exceed {MAX_CAT} characters.")
                num_errors += 1

        return num_errors
    
    @staticmethod
    def check_quantity_nop(quantity: str, errors_quantity: List[str]) -> int:
        strip_quantity = quantity.strip()
        num_errors = 0

        if not strip_quantity:
            errors_quantity.append("Quantity field can not be empty.")
            num_errors += 1
        else:
            try:
                int_quantity = int(strip_quantity)
                if int_quantity < 0:
                    errors_quantity.append("Quantity can not be negative.")
                    num_errors += 1
            except ValueError:
                errors_quantity.append("Quantity must be an integer.")
                num_errors += 1
        
        return num_errors
    
    @staticmethod
    def check_change_nop(change: str, errors_change: List[str]) -> int:
        strip_change = change.strip()
        num_errors = 0

        if not strip_change:
            errors_change.append("Change field can not be empty.")
            num_errors += 1
        else:
            try:
                int_change = int(strip_change)
                if int_change < 0:
                    errors_change.append("Change can not be negative.")
                    num_errors += 1
            except ValueError:
                errors_change.append("Change must be an integer.")
                num_errors += 1

        return num_errors
    
    @staticmethod
    def check_threshold_nop(threshold: str, errors_threshold: List[str]) -> int:
        strip_threshold = threshold.strip()
        num_errors = 0

        if not strip_threshold:
            errors_threshold.append("Threshold field can not be empty.")
            num_errors += 1
        else:
            try:
                int_threshold = int(strip_threshold)
                if int_threshold < 0:
                    errors_threshold.append("Threshold can not be negative.")
                    num_errors += 1
            except ValueError:
                errors_threshold.append("Threshold must be an integer.")
                num_errors += 1

        return num_errors
    
    @staticmethod
    def check_slot_value_nop(value: str, errors_value: List[str]) -> int:
        strip_value = value.strip().upper()
        num_errors = 0
        
        if not strip_value:
            errors_value.append("Slot Value field can not be empty.")
            num_errors += 1
        elif strip_value not in SLOT_VALUES:
            errors_value.append(f"{strip_value} not in {", ".join(SLOT_VALUES)}.")
            num_errors += 1
        
        return num_errors     
    
    # Optional
    @staticmethod
    def check_name_op(name: str, errors_name: List[str]) -> int:
        strip_name = name.strip()
        num_errors = 0

        if strip_name:
            if len(strip_name) > MAX_NAME:
                errors_name.append(f"Name field can not exceed {MAX_NAME} characters.")
                num_errors += 1
            
        return num_errors
    
    @staticmethod
    def check_price_op(price: str, errors_price: List[str]) -> int:
        strip_price = price.strip()
        num_errors = 0

        if strip_price:
            try:
                dec_price = Decimal(strip_price)

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
    def check_category_op(category: str, errors_category: List[str]) -> int:
        strip_category = category.strip()
        num_errors = 0

        if strip_category:
            if len(strip_category) > MAX_CAT:
                errors_category.append(f"Category field can not exceed {MAX_CAT} characters.")
                num_errors += 1

        return num_errors
    
    # Additional
    @staticmethod
    def check_item_main_inventory(item: Optional[Item], int_id: int, errors_id: List[str]) -> int:
        num_errors = 0

        if item is None:
            errors_id.append(f"Item {int_id} does not exist.")
            num_errors += 1
        elif item.main_inventory is None:
            errors_id.append(f"Item {int_id} does not exist in main inventory.")
            num_errors += 1

        return num_errors
    
    @staticmethod
    def check_item_vm_inventory(item: Optional[Item], int_id: int, errors_id: List[str]) -> int:
        num_errors = 0
        
        if item is None:
            errors_id.append(f"Item {int_id} does not exist.")
            num_errors += 1
        elif not item.vending_machine_slots:
            errors_id.append(f"Item {int_id} is not in the vending machine.")
            num_errors += 1
        
        return num_errors