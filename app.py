from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask import session
import smtplib
from email.message import EmailMessage
import secrets
from database import Session
import logic.user_logic as user_logic
from database import Session
from database import Session
import logic.vm_slot_logic as vm
import logic.transaction_logic as transac
import logic.user_logic as user_logic
from tables.user import Role

app = Flask(__name__)
app.secret_key = "umbc-secret-key"

# @app.route("/", methods = ['GET', 'POST'])
# def welcome():
#     global last_staff_name
#     error = None
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")

#         if not username or not password:
#             error = "Please enter both username and password."
#         else:
#             with Session() as db_session:
#                 approved_user = user_logic.get_username(db_session, username)
#                 db_session.commit()

#             session["staff_name"] = username
            
#             previous_login = username 
#             session["previous_login"] = previous_login


#             if previous_login:
#                 if hasattr(previous_login, "strftime"):
#                     session["previous_login"] = previous_login.strftime("%A, %B %d • %I:%M %p")
#                 else:
#                     session["previous_login"] = previous_login
#             else:
#                 session["previous_login"] = "First login"

#             if not approved_user:
#                 error = "Invalid staff name."
#             elif password != "umbc123":
#                 error = "Invalid password."
#             else:
#                 return redirect(url_for("dashboard"))

#     return render_template('welcome.html', error = error)

@app.route("/", methods=["GET", "POST"])
def welcome():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            error = "Please enter both username and password."
        else:
            with Session() as db_session:
                approved_user = user_logic.get_username(db_session, username)

                if not approved_user:
                    error = "Invalid staff name."
                elif password != "umbc123":
                    error = "Invalid password."
                else:
                    previous_login = user_logic.update_last_login(db_session, username)
                    db_session.commit()

                    session["staff_name"] = username
                    if previous_login:
                        if hasattr(previous_login, "strftime"):
                            session["previous_login"] = previous_login.strftime("%A, %B %d • %I:%M %p")
                        else:
                            session["previous_login"] = str(previous_login)
                    else:
                        session["previous_login"] = "First login"   
                    return redirect(url_for("dashboard"))
    
    return render_template("welcome.html", error=error)


inventory = [

    {"slot": "A1", "item": "Tissues", "quantity": 2, "price": 1.00, "max": 6},
    {"slot": "A2", "item": "Pens", "quantity": 5,"price": 1.50, "max": 5},
    {"slot": "A3", "item": "Markers", "quantity": 1, "price": 1.55, "max": 5},
    {"slot": "A4", "item": "Pencils", "quantity": 0, "price": 1.60, "max": 6},

    {"slot": "B1", "item": "Notebooks", "quantity": 4, "price": 2.00, "max": 5},
    {"slot": "B2", "item": "Sticky Notes", "quantity": 2, "price": 2.05,"max": 5},
    {"slot": "B3", "item": "Highlighters", "quantity": 5, "price": 2.10, "max": 5},
    {"slot": "B4", "item": "Erasers", "quantity": 1, "price": 2.15, "max": 5},

    {"slot": "C1", "item": "Spoons", "quantity": 3, "price": 1.75, "max": 6},
    {"slot": "C2", "item": "Forks",  "quantity": 6, "price": 1.80, "max": 6},
    {"slot": "C3", "item": "Napkins", "quantity": 0, "price": 1.85, "max": 6},
    {"slot": "C4", "item": "Wet Wipes", "quantity": 2, "price": 1.90, "max": 6},

    {"slot": "D1", "item": "Hand Sanitizer", "quantity": 3, "price": 2.50,"max": 5},
    {"slot": "D2", "item": "Bandages", "quantity": 5, "price": 2.55, "max": 5},
    {"slot": "D3", "item": "Pain Gel",  "quantity": 1, "price": 2.60, "max": 5},
    {"slot": "D4", "item": "Safety Pins", "quantity": 0, "price": 2.65, "max": 5},

    {"slot": "E1", "item": "Advil",  "quantity": 2,"price": 3.00, "max": 5},
    {"slot": "E2", "item": "Aspirin", "quantity": 5, "price": 3.05, "max": 5},
    {"slot": "E3", "item": "Cold Medicine", "quantity": 1, "price": 3.10, "max": 5},
    {"slot": "E4", "item": "Tampons", "quantity": 0, "price": 3.15, "max": 5},

    {"slot": "F1", "item": "Pads", "quantity": 3, "price": 3.20, "max": 5},
    {"slot": "F2", "item": "Comb", "quantity": 5, "price": 3.25, "max": 5},
    {"slot": "F3", "item": "Phone Charger", "quantity": 1, "price": 5.00, "max": 4},
    {"slot": "F4", "item": "Earbuds", "quantity": 4, "price": 5.50, "max": 4}

]

@app.route("/dashboard")
def dashboard():

    with Session() as db_session:
        items = vm.list_stock_status(db_session)
        
    items_out =  sum(1 for item in items if item.status.value == "OUT")
    items_low = sum(1 for item in items if item.status.value == "LOW")

    
    staff_name = session.get("staff_name", "Unknown")
    previous_staff = session.get("previous_staff", "No previous staff")
    previous_login = session.get("previous_login", "First login")
    last_checked = datetime.now().strftime("%A, %B %d • %I:%M %p")


    return render_template(
    "dashboard.html",
    items_out=items_out,
    low_items=items_low,
    staff_name=staff_name,
    last_checked = last_checked,
    previous_staff = previous_staff,
    previous_login=previous_login
)

@app.route("/stock")
def stock():
    page = request.args.get("page", 1 , type = int)

    with Session() as db_session:
        items = vm.list_stock_slot(db_session)
    
    if page == 1:
        paged_items = items[0:12]
    else:
        paged_items = items[12:24]
    return render_template('stock.html', items = paged_items, page =page) 

@app.route("/buy/<slot>")
def buy(slot):
    errors = []

    with Session() as db_session:
        try:
            slot_obj = vm.get_slot(db_session, slot, errors)

            if slot_obj is None:
                print(errors)
                return redirect(url_for("stock"))

            if slot_obj.item_price is None:
                print("Cannot buy empty slot.")
                return redirect(url_for("stock"))

            vm.purchase(db_session, str(slot_obj.item_price), "1")
            db_session.commit()

        except ValueError as e:
            db_session.rollback()
            print(e)

    return redirect(url_for("stock"))
            

@app.route("/restock")
def restock_item():
    with Session() as db_session:
        items = vm.list_stock_status(db_session)

    restock_list = [item for item in items
        if item.status.value in ["LOW", "OUT"]]
    return render_template("restock.html", items = restock_list)


@app.route("/update_item/<slot>", methods=["POST"])
def update_item(slot):
    qty = int(request.form.get("quantity"))

    with Session() as db_session:
        try:
            vm.restock(db_session, slot, qty)
            db_session.commit()
        except ValueError as e:
            db_session.rollback()
            print(e)

    return redirect(url_for("restock_item"))

@app.route("/logout")
def logout():
    last_user = session.get("staff_name")
    session.clear()
    if last_user:
        session["previous_staff"] = last_user 
    return redirect(url_for("welcome"))
 

sender = "umbctest4@gmail.com"
app_password = "fwcr omei khkw dnna"

def send_password_email(username):
    if not username:
        return "Please enter your staff username."

    with Session() as db_session:
        user_exists = user_logic.get_username(db_session, username)

    if not user_exists:
        return "User not approved."

    receiver = username + "@umbc.edu"

    msg = EmailMessage()
    msg.set_content("Your vending machine staff password is: umbc123")
    msg["Subject"] = "Vending Machine Staff Password"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.send_message(msg)

        return "Password emailed successfully."

    except Exception as e:
        return f"Error: {e}"

@app.route("/forgotpassword", methods=["GET", "POST"])
def forgot_password():
    message = None

    if request.method == "POST":
        username = request.form.get("username")
        message = send_password_email(username)

    return render_template('forgotpassword.html', message=message)


security_keys = [
    "umbc",
    "UMB-7KQ2-M9XA",
    "VEND-4PZ8-LT21",
    "KEY-6XMN-3A8F",
    "STAFF-92KD-R7QW",
    "ADMIN-J4V2-QP90"
]

def validInputs(security_key, username):
    if not security_key:
        return "Please enter the security key."

    if not username:
        return "Please enter your staff username."

    if security_key not in security_keys:
        return "Please Enter a valid Key."

    with Session() as db_session:
        try:
            user_logic.add_user(db_session, username, Role.STAFF)
            db_session.commit()

        except ValueError as e:
            db_session.rollback()
            return f"Error: {e}"

    emailreceiver = username + "@umbc.edu"

    msg = EmailMessage()
    msg.set_content("Your vending machine staff password is: umbc123")
    msg["Subject"] = "Vending Machine New User Staff Password"
    msg["From"] = sender
    msg["To"] = emailreceiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.send_message(msg)

        return "Account created. Password emailed successfully."

    except Exception as e:
        return f"Error: {e}"


@app.route("/createaccount", methods=["GET", "POST"])
def createAccount():
    message = None

    if request.method == "POST":
        security_key = request.form.get("security_key")
        username = request.form.get("username")

        message = validInputs(security_key, username)

    return render_template("createaccount.html", message=message)



if __name__ == '__main__':
    app.run(debug=True)