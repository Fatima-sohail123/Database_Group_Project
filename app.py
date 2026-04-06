from flask import Flask, render_template

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Products page
@app.route("/products")
def products():
    # empty data for now
    products = []
    suppliers = []
    return render_template("products.html", products=products, suppliers=suppliers)

# Suppliers page
@app.route("/suppliers")
def suppliers():
    suppliers = []
    return render_template("suppliers.html", suppliers=suppliers)

# Sales page
@app.route("/sales")
def sales():
    sales = []
    products = []
    return render_template("sales.html", sales=sales, products=products)

if __name__ == "__main__":
    app.run(debug=True)