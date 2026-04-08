from database import Session
import logic.item_logic as logic

DEMO_OPTIONS = ["Add Item", "Delete Item"]

def demo_create_item(session):
    name = input("Enter Item Name: ")
    category = input("Enter Item Category: ")
    price = input("Enter Item Price: ")
    print()

    try:
        logic.create_item(session, name, price, category)
        print("Item created.")
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ":", field_errors)

    session.commit()
    return

def demo_delete_item(session):
    try:
        items = logic.search_items(session, string=None)
        for item in items:
            print(item)
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ":", field_errors)
        return
    
    if not items:
        print("No items in the database.")
        return

    id_num = input("Enter Item's ID to delete: ")
    print()

    try:
        logic.delete_item(session, id_num)
        print("Item deleted.")
    except ValueError as e:
        session.rollback()
        for field, field_errors in e.args[0].items():
            print(field, ":", field_errors)

    session.commit()
    return
    
def main():
    while True:
        with Session() as session:
            for i, demo_option in enumerate(DEMO_OPTIONS, start=1):
                print(f"{i}: {demo_option}")
            print()

            option = input("Enter Option: ")

            if option == DEMO_OPTIONS[0]:
                demo_create_item(session)
            elif option == DEMO_OPTIONS[1]:
                demo_delete_item(session)
            else:
                break
    return

if __name__ == "__main__":
    main()
