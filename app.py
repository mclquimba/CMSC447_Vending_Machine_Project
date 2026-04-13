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

@app.route("/restock")
def restock():
    return render_template('restock.html')
    
if __name__ == '__main__':
    app.run(debug=True)

inventory = [

    {"slot": "A1", "item": "Tissues", "price": 1.00, "quantity": 2, "max": 6},
    {"slot": "A2", "item": "Pens", "price": 1.50, "quantity": 5, "max": 5},
    {"slot": "A3", "item": "Markers", "price": 1.55, "quantity": 1, "max": 5},
    {"slot": "A4", "item": "Pencils", "price": 1.60, "quantity": 0, "max": 6},

    {"slot": "B1", "item": "Notebooks", "price": 2.00, "quantity": 4, "max": 5},
    {"slot": "B2", "item": "Sticky Notes", "price": 2.05, "quantity": 2, "max": 5},
    {"slot": "B3", "item": "Highlighters", "price": 2.10, "quantity": 5, "max": 5},
    {"slot": "B4", "item": "Erasers", "price": 2.15, "quantity": 1, "max": 5},

    {"slot": "C1", "item": "Spoons", "price": 0.75, "quantity": 3, "max": 6},
    {"slot": "C2", "item": "Forks", "price": 0.80, "quantity": 6, "max": 6},
    {"slot": "C3", "item": "Napkins", "price": 0.85, "quantity": 0, "max": 6},
    {"slot": "C4", "item": "Wet Wipes", "price": 0.90, "quantity": 2, "max": 6},

    {"slot": "D1", "item": "Hand Sanitizer", "price": 2.50, "quantity": 3, "max": 5},
    {"slot": "D2", "item": "Bandages", "price": 2.55, "quantity": 5, "max": 5},
    {"slot": "D3", "item": "Pain Gel", "price": 2.60, "quantity": 1, "max": 5},
    {"slot": "D4", "item": "Safety Pins", "price": 2.65, "quantity": 0, "max": 5},

    {"slot": "E1", "item": "Advil", "price": 3.00, "quantity": 2, "max": 5},
    {"slot": "E2", "item": "Aspirin", "price": 3.05, "quantity": 5, "max": 5},
    {"slot": "E3", "item": "Cold Medicine", "price": 3.10, "quantity": 1, "max": 5},
    {"slot": "E4", "item": "Tampons", "price": 3.15, "quantity": 0, "max": 5},

    {"slot": "F1", "item": "Pads", "price": 3.20, "quantity": 3, "max": 5},
    {"slot": "F2", "item": "Comb", "price": 3.25, "quantity": 5, "max": 5},
    {"slot": "F3", "item": "Phone Charger", "price": 5.00, "quantity": 1, "max": 4},
    {"slot": "F4", "item": "Earbuds", "price": 5.50, "quantity": 4, "max": 4}

]

def get_status(item):
    ratio = item["quantity"] / item["max"]

    if item["quantity"] == 0:
        return "OUT"
    elif ratio < 0.8:
        return "LOW"
    else:
        return "GOOD"

    
@app.route("/stock")
def stock():
    for item in inventory:
        item["status"] = get_status(item)
    return render_template("stock.html", items = inventory) 

    
