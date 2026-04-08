from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def get_database():
    return pymysql.connect(
        host='172.31.20.27',
        user='root',
        password='Drishty2005$',
        db='InventoryDB',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    return render_template('index.html')

# --- PRODUCTS SECTION ---
@app.route('/products')
def products():
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM Products")
        products_list = cursor.fetchall()

        cursor.execute("SELECT supplier_id, name FROM Suppliers")
        suppliers_list = cursor.fetchall()
    db.close()
    return render_template('products.html', products=products_list, suppliers=suppliers_list)

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    s_id = request.form.get('supplier_id')

    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Products (name, price, quantity, supplier_id)
            VALUES (%s, %s, %s, %s)
        """, (name, price, quantity, s_id))
    db.commit()
    db.close()
    return redirect(url_for('products'))

@app.route('/edit_product/<int:id>')
def edit_product(id):
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM Products WHERE product_id = %s", (id,))
        product_data = cursor.fetchone()

        cursor.execute("SELECT supplier_id, name FROM Suppliers")
        suppliers_list = cursor.fetchall()
    db.close()
    return render_template('editpage.html', product=product_data, suppliers=suppliers_list)

@app.route('/update_product', methods=['POST'])
def update_product():
    p_id = request.form.get('product_id')
    name = request.form.get('name')
    price = request.form.get('price')
    qty = request.form.get('quantity')
    s_id = request.form.get('supplier_id')

    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("""
            UPDATE Products
            SET name=%s, price=%s, quantity=%s, supplier_id=%s
            WHERE product_id=%s
        """, (name, price, qty, s_id, p_id))
    db.commit()
    db.close()
    return redirect(url_for('products'))

@app.route('/delete_product/<int:id>')
def delete_product(id):
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM Products WHERE product_id = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('products'))

# --- SUPPLIERS SECTION ---
@app.route('/suppliers')
def suppliers():
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("SELECT supplier_id, name, phone, email FROM Suppliers")
        suppliers_list = cursor.fetchall()
    db.close()
    return render_template('suppliers.html', suppliers=suppliers_list)

@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')

    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Suppliers (name, phone, email)
            VALUES (%s, %s, %s)
        """, (name, phone, email))
    db.commit()
    db.close()
    return redirect(url_for('suppliers'))

@app.route('/edit_supplier/<int:id>')
def edit_supplier(id):
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM Suppliers WHERE supplier_id = %s", (id,))
        supplier_data = cursor.fetchone()
    db.close()
    return render_template('editsupplier.html', supplier=supplier_data)

@app.route('/update_supplier', methods=['POST'])
def update_supplier():
    s_id = request.form.get('supplier_id')
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')

    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("UPDATE Suppliers SET name=%s, phone=%s, email=%s WHERE supplier_id=%s",
                       (name, phone, email, s_id))
    db.commit()
    db.close()
    return redirect(url_for('suppliers'))

@app.route('/delete_supplier/<int:id>')
def delete_supplier(id):
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM Suppliers WHERE supplier_id = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('suppliers'))

# --- SALES SECTION ---
@app.route('/sales')
def sales():
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("SELECT product_id, name FROM Products")
        products_list = cursor.fetchall()

        cursor.execute("""
            SELECT s.sale_id, p.name AS product_name, s.quantity, s.sale_date
            FROM Sales s
            JOIN Products p ON s.product_id = p.product_id
        """)
        sales_list = cursor.fetchall()
    db.close()
    return render_template('sales.html', sales=sales_list, products=products_list)

@app.route('/add_sale', methods=['POST'])
def add_sale():
    p_id = request.form.get('product_id')
    qty = request.form.get('quantity')

    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Sales (product_id, quantity, user_id)
            VALUES (%s, %s, %s)
        """, (p_id, qty, 1))
    db.commit()
    db.close()
    return redirect(url_for('sales'))

@app.route('/delete_sale/<int:id>')
def delete_sale(id):
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM Sales WHERE sale_id = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('sales'))

# --- USERS SECTION ---
@app.route('/users')
def users():
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("SELECT user_id, name, email, role FROM Users")
        users_list = cursor.fetchall()
    db.close()
    return render_template('users.html', users=users_list)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role')

    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Users (name, email, role)
            VALUES (%s, %s, %s)
        """, (name, email, role))
    db.commit()
    db.close()
    return redirect(url_for('users'))

@app.route('/edit_user/<int:id>')
def edit_user(id):
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM Users WHERE user_id = %s", (id,))
        user_data = cursor.fetchone()
    db.close()
    return render_template('edituser.html', user=user_data)

@app.route('/update_user', methods=['POST'])
def update_user():
    u_id = request.form.get('user_id')
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role')

    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("""
            UPDATE Users
            SET name=%s, email=%s, role=%s
            WHERE user_id=%s
        """, (name, email, role, u_id))
    db.commit()
    db.close()
    return redirect(url_for('users'))

@app.route('/delete_user/<int:id>')
def delete_user(id):
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM Users WHERE user_id = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('users'))

# --- ORDERS SECTION ---
@app.route('/orders')
def orders():
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT o.order_id, p.name AS product_name, s.name AS supplier_name,
                   o.quantity, o.order_date
            FROM Orders o
            LEFT JOIN Products p ON o.product_id = p.product_id
            LEFT JOIN Suppliers s ON p.supplier_id = s.supplier_id
        """)
        orders_list = cursor.fetchall()

        cursor.execute("SELECT product_id, name FROM Products")
        products_list = cursor.fetchall()

        cursor.execute("SELECT supplier_id, name FROM Suppliers")
        suppliers_list = cursor.fetchall()
    db.close()
    return render_template('orders.html', orders=orders_list, products=products_list, suppliers=suppliers_list)

@app.route('/add_order', methods=['POST'])
def add_order():
    p_id = request.form.get('product_id')
    qty = request.form.get('quantity')

    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Orders (product_id, quantity, user_id)
            VALUES (%s, %s, %s)
        """, (p_id, qty, 1))
    db.commit()
    db.close()
    return redirect(url_for('orders'))

@app.route('/delete_order/<int:id>')
def delete_order(id):
    db = get_database()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM Orders WHERE order_id = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('orders'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)