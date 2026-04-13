from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def welcome():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            error = "Please enter both username and password."
        elif password != "umbc123":
            error = "Invalid password."
        else:
            return redirect(url_for("dashboard"))
    return render_template('welcome.html', error = error)

@app.route("/dashboard")
def dashboard():
    items_out = 6
    low_items = 4
    last_checked = "4/8/26 10:30PM"
    staff_name = "UMBC3212"
    
    return render_template("dashboard.html", items_out = items_out, low_items = low_items, last_checked = last_checked, staff_name = staff_name)

# @app.route("/restock")
# def restock():
#     return render_template('restock.html')

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

    
@app.route("/stock")
def stock():
    for item in inventory:
        item["status"] = get_status(item)
    return render_template('stock.html', items = inventory) 

    
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

if __name__ == '__main__':
    app.run(debug=True)