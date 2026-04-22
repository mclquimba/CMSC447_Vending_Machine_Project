from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask import session


app = Flask(__name__)
app.secret_key = "umbc-secret-key"

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

    last_checked = datetime.now().strftime("%A, %B %d • %I:%M %p")
    staff_name = session.get("staff_name", "Unknown")
    previous_staff = last_staff_name

    return render_template(
    "dashboard.html",
    items_out=items_out,
    low_items=items_low,
    last_checked=last_checked,
    staff_name=staff_name,
    previous_staff=previous_staff
)

@app.route("/stock")
def stock():
    page = request.args.get("page", 1 , type = int)

    for item in inventory:
        item["status"] = get_status(item)
    
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

@app.route("/forgot-password")
def forgot_password():
    return redirect("https://forms.gle/UQewp7yneGsjfZ6M9")
if __name__ == '__main__':
    app.run(debug=True)