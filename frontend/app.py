from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask import session
import smtplib
from email.message import EmailMessage
#from logic.modification_logic import 
import secrets


app = Flask(__name__)
app.secret_key = "umbc-secret-key"
approved_users = ["staff123", "umbcislove1", "UMBC3212","apascal1"]


@app.route("/", methods = ['GET', 'POST'])
def welcome():
    global last_staff_name
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            error = "Please enter both username and password."
        elif password != "umbc123":
            error = "Invalid password."
        else:
            session["staff_name"] = username 
            last_staff_name = username 
            return redirect(url_for("dashboard"))

    return render_template('welcome.html', error = error)

    def newWelcome():
        while True:
            try: 
                if request.method == "POST":
                    username = request.form.get("username")
                    password = request.form.get("passwowrd")
                break
            except ValueError:
                print("Invalid password please try again")

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

def get_status(item):
    ratio = item["quantity"] / item["max"]

    if item["quantity"] == 0:
        return "OUT"
    elif ratio < 0.5:
        return "LOW"
    else:
        return "GOOD"

@app.route("/dashboard")
def dashboard():
    items_out = 0
    items_low = 0

    for item in inventory:
        item["status"] = get_status(item)

        if item["status"] == "OUT":
            items_out += 1
        elif item["status"] == "LOW":
            items_low += 1
    
    user_sessions = {}
    staff_name = session.get("staff_name", "Unknown")
    last_login = user_sessions.get(staff_name) 
    user_sessions[staff_name] = datetime.now()

    if last_login:
        time_diff = datetime.now() - last_login
        current_time_str = datetime.now().strftime("%A, %B %d • %I:%M %p")


    
    previous_staff = staff_name

    return render_template(
    "dashboard.html",
    items_out=items_out,
    low_items=items_low,
    last_login=last_login,
    staff_name=staff_name,
    previous_staff=previous_staff
)

@app.route("/stock")
def stock():
    page = request.args.get("page", 1 , type = int)

    for item in inventory:
        item["status"] = get_status(item)

        if item["quantity"] == 0:
            item["name"] = "empty"
    
    if page == 1:
        items = inventory[0:12]
    else:
        items = inventory[12:24]
    return render_template('stock.html', items = items, page =page) 

    
@app.route("/buy/<slot>")
def buy(slot):
    for item in inventory:
        if item["slot"] == slot:
            if item["quantity"] > 0:
                item["quantity"] -= 1
                break
    return redirect(url_for("stock"))
            
@app.route("/restock")
def restock_item():
    restock_list = []
    for item in inventory:
        item["status"] = get_status(item)
        if item["status"] in ["LOW","OUT"]:
            restock_list.append(item)
    return render_template("restock.html", items = restock_list)

@app.route("/update_item/<slot>", methods=["POST"])
def update_item(slot):

    for item in inventory:
        if item["slot"] == slot:

            qty = int(request.form.get("quantity"))
            max_val = int(request.form.get("max"))

            if qty < 0:
                qty = 0

            if qty > max_val:
                qty = max_val

            item["quantity"] = qty
            item["max"] = max_val
            item["status"] = get_status(item)

            break

    return redirect(url_for("restock_item"))
        
@app.route("/logout")
def logout():
    session.clear()   
    return redirect(url_for("welcome"))
 


sender = "umbctest4@gmail.com"
app_password = "fwcr omei khkw dnna"

approved_users = ["staff123", "umbcislove1", "UMBC3212","apascal1"]


def send_password_email(username):
    if username not in approved_users:
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
    "UMB-7KQ2-M9XA",
    "VEND-4PZ8-LT21",
    "KEY-6XMN-3A8F",
    "STAFF-92KD-R7QW",
    "ADMIN-J4V2-QP90"
]

approved_users = []

def validInputs(security_key, username):
    if not security_key:
        return "Please enter the security key."

    if not username:
        return "Please enter your staff username."

    if security_key not in security_keys:
        return "Please Enter a valid Key."

    if not username:
        return "Please enter a username."


    if username in approved_users:
        return "This user already exists."

    approved_users.append(username)

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