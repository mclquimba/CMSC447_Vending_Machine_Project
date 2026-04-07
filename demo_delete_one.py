from logic.item_logic import delete_item, get_item_name
from database import Session
from demo_constants import DEMO_NAME_1

def main():
    with Session() as session:
        todelete = get_item_name(session, DEMO_NAME_1)
        item = delete_item(session, str(todelete.id))
        if item is not None:
            print(item)
        session.commit()

if __name__ == "__main__":
    main()