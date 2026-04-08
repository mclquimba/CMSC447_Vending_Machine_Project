from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/dashboard.html")
def dashboard():
    return render_template('dashboard.html')

@app.route("/stock.html")
def stock():
    return render_template('stock.html')
@app.route("restock.html")
def restock():
    return render_template('restock.html')
    
if __name__ == '__main__':
    app.run(debug=True)





    
