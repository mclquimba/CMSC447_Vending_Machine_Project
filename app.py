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

@app.route("/stock")
def stock():
    return render_template('stock.html')
@app.route("/restock")
def restock():
    return render_template('restock.html')
    
if __name__ == '__main__':
    app.run(debug=True)





    
