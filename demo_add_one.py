from database import Session

from logic.item_logic import create_item
from logic.main_inventory_logic import add_stock

from demo_constants import DEMO_NAME_1, DEMO_PRICE_1, DEMO_CAT_1, DEMO_QUANTITY_1, DEMO_THRESH_1

def main():
    with Session() as session:
        item = create_item(session, DEMO_NAME_1, DEMO_PRICE_1, DEMO_CAT_1)
        session.commit()
    print("Item created.")

if __name__ == "__main__":
    main()