from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from sqlalchemy import select
from flask import session
import smtplib
import os
from dotenv import load_dotenv
import logic.email_logic as email_logic
from email.message import EmailMessage
import logic.transaction_logic as transaction_logic
import secrets
from tables.user import User, Role
from database import Session
from tables.transaction import Transaction
from sqlalchemy import select
import logic.user_logic as user_logic
from database import Session
from database import Session
import logic.vm_slot_logic as vm
import logic.transaction_logic as transac
import logic.user_logic as user_logic
from tables.user import Role

app = Flask(__name__)
app.secret_key = "umbc-secret-key"

load_dotenv()
ADMIN_ACCESS_KEY = os.getenv("ADMIN_ACCESS_KEY")

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
    username= " "
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
    
    return render_template("welcome.html", error=error, username = username)

def get_restock_alert_count():
    with Session() as db_session:
        items = vm.list_stock_slot(db_session)

    return sum(
        1 for item in items
        if item.item_name and item.status.value in ["LOW", "OUT"]
    )

# inventory = [

#     {"slot": "A1", "item": "Tissues", "quantity": 2, "price": 1.00, "max": 6},
#     {"slot": "A2", "item": "Pens", "quantity": 5,"price": 1.50, "max": 5},
#     {"slot": "A3", "item": "Markers", "quantity": 1, "price": 1.55, "max": 5},
#     {"slot": "A4", "item": "Pencils", "quantity": 0, "price": 1.60, "max": 6},

#     {"slot": "B1", "item": "Notebooks", "quantity": 4, "price": 2.00, "max": 5},
#     {"slot": "B2", "item": "Sticky Notes", "quantity": 2, "price": 2.05,"max": 5},
#     {"slot": "B3", "item": "Highlighters", "quantity": 5, "price": 2.10, "max": 5},
#     {"slot": "B4", "item": "Erasers", "quantity": 1, "price": 2.15, "max": 5},

#     {"slot": "C1", "item": "Spoons", "quantity": 3, "price": 1.75, "max": 6},
#     {"slot": "C2", "item": "Forks",  "quantity": 6, "price": 1.80, "max": 6},
#     {"slot": "C3", "item": "Napkins", "quantity": 0, "price": 1.85, "max": 6},
#     {"slot": "C4", "item": "Wet Wipes", "quantity": 2, "price": 1.90, "max": 6},

#     {"slot": "D1", "item": "Hand Sanitizer", "quantity": 3, "price": 2.50,"max": 5},
#     {"slot": "D2", "item": "Bandages", "quantity": 5, "price": 2.55, "max": 5},
#     {"slot": "D3", "item": "Pain Gel",  "quantity": 1, "price": 2.60, "max": 5},
#     {"slot": "D4", "item": "Safety Pins", "quantity": 0, "price": 2.65, "max": 5},

#     {"slot": "E1", "item": "Advil",  "quantity": 2,"price": 3.00, "max": 5},
#     {"slot": "E2", "item": "Aspirin", "quantity": 5, "price": 3.05, "max": 5},
#     {"slot": "E3", "item": "Cold Medicine", "quantity": 1, "price": 3.10, "max": 5},
#     {"slot": "E4", "item": "Tampons", "quantity": 0, "price": 3.15, "max": 5},

#     {"slot": "F1", "item": "Pads", "quantity": 3, "price": 3.20, "max": 5},
#     {"slot": "F2", "item": "Comb", "quantity": 5, "price": 3.25, "max": 5},
#     {"slot": "F3", "item": "Phone Charger", "quantity": 1, "price": 5.00, "max": 4},
#     {"slot": "F4", "item": "Earbuds", "quantity": 4, "price": 5.50, "max": 4}
 
# ]

@app.route("/dashboard")
def dashboard():
    with Session() as db_session:
        items = vm.list_stock_slot(db_session)

    total_items = len(items)

    items_good = sum(1 for item in items if item.status.value == "GOOD")
    items_low = sum(1 for item in items if item.status.value == "LOW")
    items_out = sum(1 for item in items if item.status.value == "OUT")

    good_percent = round((items_good / total_items) * 100) if total_items > 0 else 0
    low_percent = round((items_low / total_items) * 100) if total_items > 0 else 0
    out_percent = round((items_out / total_items) * 100) if total_items > 0 else 0


    restock_alerts = get_restock_alert_count()

    staff_name = session.get("staff_name", "Unknown")
    previous_staff = session.get("previous_staff", "No previous staff")
    previous_login = session.get("previous_login", "First login")
    last_checked = datetime.now().strftime("%A, %B %d • %I:%M %p")

    return render_template(
        "dashboard.html",
        items_out=items_out,
        low_items=items_low,
        items_good=items_good,
        total_items=total_items,
        good_percent=good_percent,
        low_percent=low_percent,
        out_percent=out_percent,
        restock_alerts=restock_alerts,
        staff_name=staff_name,
        previous_staff=previous_staff,
        previous_login=previous_login,
        last_checked=last_checked
    )
# @app.route("/dashboard")
# def dashboard():
#     restock_alerts = get_restock_alert_count()
#     with Session() as db_session:
#         items = vm.list_stock_status(db_session)
    
#     total_items = len(items)
        
#     items_out =  sum(1 for item in items if item.status.value == "OUT")
#     items_low = sum(1 for item in items if item.status.value == "LOW")

    
#     staff_name = session.get("staff_name", "Unknown")
#     previous_staff = session.get("previous_staff", "No previous staff")
#     previous_login = session.get("previous_login", "First login")
#     last_checked = datetime.now().strftime("%A, %B %d • %I:%M %p")


#     return render_template(
#     "dashboard.html",
#     items_out=items_out,
#     low_items=items_low,
#     staff_name=staff_name,
#     last_checked = last_checked,
#     previous_staff = previous_staff,
#     previous_login=previous_login,
#         restock_alerts=restock_alerts

# )

@app.route("/stock")
def stock():
    restock_alerts = get_restock_alert_count()
    page = request.args.get("page", 1 , type = int)

    with Session() as db_session:
        items = vm.list_stock_slot(db_session)
    
    if page == 1:
        paged_items = items[0:12]
    else:
        paged_items = items[12:24]
    return render_template('stock.html', items = paged_items, page =page, restock_alerts=restock_alerts
) 

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
            transaction_logic.record_transaction(
                db_session,
                str(slot_obj.item_price),
                "1"
            )

            db_session.commit()
            email_logic.check_and_send_auto_restock_alert()

        except ValueError as e:
            db_session.rollback()
            print(e)

    return redirect(url_for("stock"))
            

# @app.route("/restock")
# def restock_item():
#     with Session() as db_session:
#         items = vm.list_stock_status(db_session)

#     restock_list = [item for item in items
#         if item.status.value in ["LOW", "OUT"]]
#     return render_template("restock.html", items = restock_list)

@app.route("/restock")
def restock_item():
    with Session() as db_session:
        all_items = vm.list_stock_slot(db_session)

    restock_list = [
        item for item in all_items
        if item.item_name and item.status.value in ["LOW", "OUT"]
    ]

    restock_alerts = len(restock_list)

    return render_template(
        "restock.html",
        items=restock_list,
        restock_alerts=restock_alerts
    )




# @app.route("/update_item/<slot>", methods=["POST"])
# def update_item(slot):
#     qty = int(request.form.get("quantity"))

#     with Session() as db_session:
#         try:
#             vm.restock(db_session, slot, qty)
#             db_session.commit()
#         except ValueError as e:
#             db_session.rollback()
#             print(e)

#     return redirect(url_for("restock_item"))
@app.route("/update_item/<slot>", methods=["POST"])
def update_item(slot):
    amount = request.form.get("amount")

    with Session() as db_session:
        try:
            vm.restock(db_session, slot, amount)
            db_session.commit()
            email_logic.check_and_send_auto_restock_alert()
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

# def get_all_staff_emails():
#     with Session() as db_session:
#         users = db_session.scalars(select(User)).all()

#     staff_emails = []

#     for user in users:
#         staff_emails.append(user.username + "@umbc.edu")

#     return staff_emails

       
# def send_restock_alert_email(alert_type="Manual"):
#     with Session() as db_session:
#         items = vm.list_stock_slot(db_session)

#     out_items = [
#         item for item in items
#         if item.item_name and item.status.value == "OUT"
#     ]

#     low_items = [
#         item for item in items
#         if item.item_name and item.status.value == "LOW"
#     ]

#     recipients = get_all_staff_emails()

#     if not recipients:
#         return "No staff emails found."

#     email_body = f"Vending Machine Restock Alert ({alert_type})\n\n"

#     email_body += f"Out-of-stock items: {len(out_items)}\n"
#     email_body += f"Low-stock items: {len(low_items)}\n\n"

#     email_body += "Alert rule:\n"
#     email_body += "- Auto alert triggers when OUT items are 5 or more OR LOW items are more than 10.\n\n"

#     email_body += "Items needing attention:\n"

#     for item in out_items:
#         email_body += f"- {item.slot_value}: {item.item_name} is OUT\n"

#     for item in low_items:
#         email_body += f"- {item.slot_value}: {item.item_name} has {item.quantity_cur}/{item.quantity_max} remaining\n"

#     msg = EmailMessage()
#     msg.set_content(email_body)
#     msg["Subject"] = f"Vending Machine Restock Alert - {alert_type}"
#     msg["From"] = sender
#     msg["To"] = ", ".join(recipients)

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(sender, app_password)
#             server.send_message(msg)

#         return f"{alert_type} restock alert email sent successfully."

#     except Exception as e:
#         return f"Error sending email: {e}"

@app.route("/reports", methods=["GET", "POST"])
def reports():
    message = None

    out_threshold = email_logic.OUT_THRESHOLD
    low_threshold = email_logic.LOW_THRESHOLD

    out_items, low_items = email_logic.get_alert_items()

    out_count = len(out_items)
    low_count = len(low_items)
    restock_alerts = out_count + low_count

    critical_alert = email_logic.is_critical_alert(out_count, low_count)

    # Manual email button
    if request.method == "POST":
        message = email_logic.send_restock_alert_email("Manual")

    # Automatic email logic
    elif critical_alert:
        if not email_logic.automatic_email_sent_today():
            message = email_logic.send_restock_alert_email("Automatic")
        else:
            message = "Critical alert active. Automatic email was already sent today."

    else:
        message = "No critical alert. Email not sent automatically."

    email_logs = email_logic.get_recent_email_logs()

    return render_template(
        "reports.html",
        out_items=out_items,
        low_items=low_items,
        out_count=out_count,
        low_count=low_count,
        out_threshold=out_threshold,
        low_threshold=low_threshold,
        critical_alert=critical_alert,
        restock_alerts=restock_alerts,
        email_logs=email_logs,
        message=message
    )

@app.route("/transactions")
def transactions():
    restock_alerts = get_restock_alert_count()

    with Session() as db_session:
        transaction_records = db_session.scalars(
            select(Transaction).order_by(Transaction.timestamp.desc())
        ).all()

    return render_template(
        "transactions.html",
        transactions=transaction_records,
        restock_alerts=restock_alerts
    )
 

@app.route("/staff", methods=["GET", "POST"])
def staff():
    message = f"Can not delete user with role{Role.ADMIN}"

    username = session.get("staff_name")

    if not username:
        return redirect(url_for("welcome"))

    with Session() as db_session:
        current_user = user_logic.get_user(db_session, username)
        admin_status = user_logic.is_admin(db_session, username)
        users = user_logic.list_users(db_session) if admin_status else []

        if request.method == "POST":
            admin_key = request.form.get("admin_key")

            if admin_key == ADMIN_ACCESS_KEY:
                user_logic.promote_user_to_admin(db_session, username)
                db_session.commit()

                message = "Admin access granted."
                admin_status = True
                users = user_logic.list_users(db_session)
            else:
                message = "Invalid admin key."
            
            if current_user == "ADMIN":
                newuser = allowAdmintocreate()
                
    restock_alerts = get_restock_alert_count()

    return render_template(
        "staff.html",
        current_user=current_user,
        admin_status=admin_status,
        users=users,
        message=message,
        restock_alerts=restock_alerts
    )

@app.route("/staff/delete/<user_id>", methods=["POST"])
def delete_staff_user(user_id):

    error_msg = "Invalid"
    username = session.get("staff_name")

    if not username:
        return redirect(url_for("welcome"))

    with Session() as db_session:
        if not  user_logic.is_admin(db_session, username):
            return redirect(url_for("staff"))

        try:
            user_logic.delete_user(db_session, user_id)
            db_session.commit()
        except ValueError as e:
            db_session.rollback()
            print(e)
    if user.role == Role.ADMIN:
        flash("Cannot delete admin")
        return redirect(url_for("staff"))
    #print(errors)
    return redirect(url_for("staff"))
    # return render_template("staff.html", error = error_msg)



if __name__ == '__main__':
    app.run(debug=True)