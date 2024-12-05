from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import random
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

app.secret_key = 'secret_key'

# Path to your database file
#DATABASE = "Checkpoint2-dbase.sqlite3"
DATABASE = "tpch.sqlite3"

# Function to connect to the database
def open_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

@app.route('/')
def home():
    if 'customer_id' not in session:
        return redirect(url_for('login'))
    return render_template('main.html', customer_id=session['customer_id'], email=session['email'])

#login for customer
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        email = request.form.get('email')
        print(f"Login Attempt: CustomerID = {customer_id}, Email = {email}")

        # Connect to the database and validate the credentials
        conn = open_connection()
        if conn:
            cursor = conn.cursor()
            #find the matching customer
            sql = "SELECT * FROM Customer WHERE CustomerID = ? AND Email = ?"
            cursor.execute(sql, (customer_id, email))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['customer_id'] = user[0]  
                session['email'] = user[2]       
                flash('Login successful!', 'success')
                print('Login sucessful')
                return redirect(url_for('home'))
            else:
                flash('Invalid ID or email!', 'danger')

    return render_template('login.html') 

#login for staff
@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        email = request.form.get('email')
        print(f"Staff Login Attempt: StaffID = {staff_id}, Email = {email}")

        conn = open_connection()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM Staff WHERE StaffID = ? AND Email = ?"
            cursor.execute(sql, (staff_id, email))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['staff_id'] = user[0]
                session['user_type'] = 'Staff'
                flash('Staff login successful!', 'success')
                print('Login sucessful')
                return redirect(url_for('mainStaff'))
            else:
                flash('Invalid ID or email for Staff!', 'danger')

    return render_template('staff_login.html') 

#login for supplier
@app.route('/supplier_login', methods=['GET', 'POST'])
def supplier_login():
    if request.method == 'POST':
        supplier_id = request.form.get('supplier_id')
        email = request.form.get('email')
        print(f"Supplier Login Attempt: SupplierID = {supplier_id}, Email = {email}")

        conn = open_connection()
        if conn:
            cursor = conn.cursor()
            #match the id and email
            sql = "SELECT * FROM Supplier WHERE SupplierID = ? AND ContactInfo = ?"
            cursor.execute(sql, (supplier_id, email))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['supplier_id'] = user[0]
                session['user_type'] = 'Supplier'
                flash('Supplier login successful!', 'success')
                print('Login sucessful')
                return redirect(url_for('mainSupplier')) 
            else:
                flash('Invalid ID or email for Supplier!', 'danger')

    return render_template('supplier_login.html')

#logout of page
@app.route('/logout')
def logout():
    session.clear() 
    flash('You have been logged out!', 'info')
    print('User logged out')
    return redirect(url_for('login'))

#route to supplier page
@app.route('/mainSupplier')
def mainSupplier():
    if 'supplier_id' not in session:
        flash('Unauthorized access! Please log in.', 'danger')
        return redirect(url_for('supplier_login'))
    supplier_id = session.get('supplier_id')
    return render_template('mainSupplier.html', supplier_id=supplier_id)

#route to staff page
@app.route('/mainStaff')
def mainStaff():
    if 'staff_id' not in session:
        flash('Unauthorized access! Please log in.', 'danger')
        return redirect(url_for('staff_login'))
    staff_id = session.get('staff_id')
    return render_template('mainStaff.html', staff_id=staff_id)

#staff update product
@app.route('/update_product', methods=['GET', 'POST'])
def update_product():
    if 'staff_id' not in session:
        flash('Unauthorized access! Please log in.', 'danger')
        return redirect(url_for('staff_login'))

    conn = open_connection()

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')
        stock_quantity = request.form.get('stock_quantity')

        if conn:
            cursor = conn.cursor()
            sql = """
            UPDATE Product
            SET Name = ?, Price = ?, Category = ?, StockQuantity = ?
            WHERE ProductID = ?;
            """
            cursor.execute(sql, (name, price, category, stock_quantity, product_id))
            conn.commit()
            conn.close()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('mainStaff'))

    else:
        cursor = conn.cursor()
        sql = "SELECT ProductID FROM Product"
        cursor.execute(sql)
        product_ids = [row[0] for row in cursor.fetchall()]

        product_id = request.args.get('product_id', type=int)
        product = None
        if product_id:
            sql = "SELECT * FROM Product WHERE ProductID = ?"
            cursor.execute(sql, (product_id,))
            product = cursor.fetchone()
        conn.close()
        return render_template('update_product.html', product_ids=product_ids, product=product, selected_product_id=product_id)


#staff remove products
@app.route('/remove_product', methods=['GET', 'POST'])
def remove_product():
    if 'staff_id' not in session:
        flash('Unauthorized access! Please log in.', 'danger')
        return redirect(url_for('staff_login'))

    conn = open_connection()

    if request.method == 'POST':
        product_id = request.form.get('product_id')

        if conn:
            try:
                cursor = conn.cursor()
                #delete product from id selected
                sql = "DELETE FROM Product WHERE ProductID = ?;"
                cursor.execute(sql, (product_id,))
                conn.commit()
                flash(f'Product with ID {product_id} removed successfully!', 'success')
            except sqlite3.Error as e:
                conn.rollback()
                flash(f'Database error: {e}', 'danger')
            finally:
                conn.close()
            return redirect(url_for('mainStaff'))

    else:
        cursor = conn.cursor()
        sql = "SELECT ProductID, Name FROM Product"
        cursor.execute(sql)
        products = cursor.fetchall() 
        conn.close()

        return render_template('remove_product.html', products=products)

#staff update order
@app.route('/update_order', methods=['GET', 'POST'])
def update_order():
    if 'staff_id' not in session:
        flash('Unauthorized access! Please log in.', 'danger')
        return redirect(url_for('staff_login'))

    conn = open_connection()

    if request.method == 'POST':
        order_id = request.form.get('order_id')
        shipping_address = request.form.get('shipping_address')
        total_amount = request.form.get('total_amount')

        if conn:
            cursor = conn.cursor()
            sql = """
            UPDATE `Order`
            SET ShippingAddress = ?, TotalAmount = ?
            WHERE OrderID = ?;
            """
            cursor.execute(sql, (shipping_address, total_amount, order_id))
            conn.commit()
            conn.close()
            flash('Order updated successfully!', 'success')
            return redirect(url_for('mainStaff'))

    else:
        cursor = conn.cursor()
        sql = "SELECT OrderID FROM `Order`"
        cursor.execute(sql)
        order_ids = [row[0] for row in cursor.fetchall()]
        order_id = request.args.get('order_id', type=int)
        order = None
        if order_id:
            sql = "SELECT * FROM `Order` WHERE OrderID = ?"
            cursor.execute(sql, (order_id,))
            order = cursor.fetchone()
        conn.close()

        return render_template('update_order.html', order_ids=order_ids, order=order, selected_order_id=order_id)

#staff remove order
@app.route('/remove_order', methods=['GET', 'POST'])
def remove_order():
    if 'staff_id' not in session:
        flash('Unauthorized access! Please log in.', 'danger')
        return redirect(url_for('staff_login'))

    conn = open_connection()

    if request.method == 'POST':
        order_id = request.form.get('order_id')

        if conn:
            try:
                cursor = conn.cursor()
                #delete all other corresponding links
                cursor.execute("DELETE FROM OrderProduct WHERE OrderID = ?;", (order_id,))
                cursor.execute("DELETE FROM Shipment WHERE OrderID = ?;", (order_id,))
                cursor.execute("DELETE FROM `Order` WHERE OrderID = ?;", (order_id,))
                conn.commit()
                flash(f'Order with ID {order_id} removed successfully!', 'success')
            except sqlite3.Error as e:
                conn.rollback()
                flash(f'Database error: {e}', 'danger')
            finally:
                conn.close()
            return redirect(url_for('mainStaff'))

    else:
        cursor = conn.cursor()
        sql = "SELECT OrderID, CustomerID FROM `Order`"
        cursor.execute(sql)
        orders = cursor.fetchall()
        conn.close()

        return render_template('remove_order.html', orders=orders)

#staff update/change shipment
@app.route('/update_shipment', methods=['GET', 'POST'])
def update_shipment():
    if 'staff_id' not in session:
        flash('Unauthorized access! Please log in.', 'danger')
        return redirect(url_for('staff_login'))

    conn = open_connection()

    if request.method == 'POST':
        shipment_id = request.form.get('shipment_id')
        shipment_date = request.form.get('shipment_date')
        status = request.form.get('status')

        if conn:
            cursor = conn.cursor()
            #update shipment based on entered data and selected id
            sql = """
            UPDATE Shipment
            SET ShipmentDate = ?, Status = ?
            WHERE ShipmentID = ?;
            """
            cursor.execute(sql, (shipment_date, status, shipment_id))
            conn.commit()
            conn.close()
            flash('Shipment updated successfully!', 'success')
            return redirect(url_for('mainStaff'))

    else:
        cursor = conn.cursor()
        sql = "SELECT ShipmentID FROM Shipment"
        cursor.execute(sql)
        shipment_ids = [row[0] for row in cursor.fetchall()]

        shipment_id = request.args.get('shipment_id', type=int)
        shipment = None
        if shipment_id:
            sql = "SELECT * FROM Shipment WHERE ShipmentID = ?"
            cursor.execute(sql, (shipment_id,))
            shipment = cursor.fetchone()
        conn.close()

        return render_template('update_shipment.html', shipment_ids=shipment_ids, shipment=shipment, selected_shipment_id=shipment_id)

#staff remove shipment
@app.route('/remove_shipment', methods=['GET', 'POST'])
def remove_shipment():
    if 'staff_id' not in session:
        flash('Unauthorized access! Please log in.', 'danger')
        return redirect(url_for('staff_login'))

    conn = open_connection()

    if request.method == 'POST':
        shipment_id = request.form.get('shipment_id')

        if conn:
            try:
                cursor = conn.cursor()
                sql = "DELETE FROM Shipment WHERE ShipmentID = ?;"
                cursor.execute(sql, (shipment_id,))
                conn.commit()
                flash(f'Shipment with ID {shipment_id} removed successfully!', 'success')
            except sqlite3.Error as e:
                conn.rollback()
                flash(f'Database error: {e}', 'danger')
            finally:
                conn.close()
            return redirect(url_for('mainStaff'))

    else:
        cursor = conn.cursor()
        sql = "SELECT ShipmentID, OrderID FROM Shipment"
        cursor.execute(sql)
        shipments = cursor.fetchall()
        conn.close()

        return render_template('remove_shipment.html', shipments=shipments)

#get all items from inventory
@app.route('/product', methods=['GET'])
def get_products():
    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            #get all products
            sql = """
                SELECT ProductID, Name, Price, Category, StockQuantity
                FROM Product
                WHERE StockQuantity > 0;
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            products = []
            for row in results:
                products.append({
                    'ProductID': row[0], 
                    'Name': row[1],
                    'Price': row[2],
                    'Category': row[3],
                    'StockQuantity': row[4]
                })
            conn.close()
            return jsonify(products), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Connection failed"}), 500

#find products with price higher than 500
@app.route('/products/high-price', methods=['GET'])
def get_high_price():
    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            #get all product more than 500
            sql = """
                SELECT ProductID, Name, Price, Category, StockQuantity
                FROM Product
                WHERE Price > 500
                ORDER BY Price DESC;
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            high_price_products = []
            for row in results:
                high_price_products.append({
                    'ProductID': row[0],
                    'Name': row[1],
                    'Price': row[2],
                    'Category': row[3],
                    'StockQuantity' : row[4]
                })

            conn.close()
            return jsonify(high_price_products), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Connection failed"}), 500


#order products by price from cheapest
@app.route('/products/ordered-by-price', methods=['GET'])
def get_products_ordered_by_price():
    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            #get all products ordered by cheapest to most expensive
            sql = """
                SELECT * 
                FROM Product
                ORDER BY Price ASC;
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]
            ordered_products = [dict(zip(column_names, row)) for row in results]

            return jsonify(ordered_products), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()
    return jsonify({"error": "Connection failed"}), 500

#allow user to view their order
@app.route('/my-orders', methods=['GET'])
def my_orders():
    if 'customer_id' not in session:
        flash("You must be logged in to view your orders.")
        return redirect(url_for('login'))

    customer_id = session['customer_id']

    conn = open_connection()
    orders = []
    if conn:
        cursor = conn.cursor()
        sql = """
        SELECT 
            o.OrderID AS OrderID, 
            o.OrderDate AS OrderDate, 
            Product.Name AS ProductName, 
            OrderProduct.Quantity AS Quantity, 
            (Product.Price * OrderProduct.Quantity) AS ProductTotal,
            Shipment.Status AS ShipmentStatus
        FROM `Order` o
        JOIN OrderProduct ON OrderProduct.OrderID = o.OrderID
        JOIN Product ON OrderProduct.ProductID = Product.ProductID
        LEFT JOIN Shipment ON o.OrderID = Shipment.OrderID
        WHERE o.CustomerID = ?
        ORDER BY o.OrderDate DESC, Product.Name ASC;
        """
        cursor.execute(sql, (customer_id,))
        results = cursor.fetchall()
        conn.close()

        for row in results:
            orders.append({
                'OrderID': row[0],
                'OrderDate': row[1],
                'ProductName': row[2],
                'Quantity': row[3],
                'ProductTotal': row[4],
                'ShipmentStatus': row[5]
            })

    return render_template('my_orders.html', orders=orders)

#get products by category
@app.route('/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            #get product based on category
            sql = """
                SELECT ProductID, Name, Category, Price, StockQuantity
                FROM Product
                WHERE Product.Category = ?
                ORDER BY Product.ProductID;
            """
            cursor.execute(sql, (category,))
            results = cursor.fetchall()

            products_by_category = []
            for row in results:
                products_by_category.append({
                    'ProductID': row[0],
                    'Name': row[1],
                    'Category': row[2],
                    'Price': row[3],
                    'StockQuantity': row[4]
                })

            conn.close()
            return jsonify(products_by_category), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Connection failed"}), 500

#customer places order
@app.route('/place-order', methods=['POST'])
def place_order():
    if 'customer_id' not in session:
        return jsonify({'message': 'You must be logged in to place an order'}), 403

    order_data = request.json
    customer_id = session['customer_id']

    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            #get the current customer based on id
            cursor.execute("SELECT Address FROM Customer WHERE CustomerID = ?", (customer_id,))
            customer = cursor.fetchone()
            if not customer:
                raise ValueError("Customer not found")
            shipping_address = customer[0]

            #creating new order
            cursor.execute(
                "INSERT INTO `Order` (OrderDate, TotalAmount, ShippingAddress, CustomerID) VALUES (DATE('now'), 0, ?, ?)",
                (shipping_address, customer_id)
            )
            order_id = cursor.lastrowid 
            print(f"Order Created in DB: OrderID={order_id}, ShippingAddress={shipping_address}")

            total_amount = 0
            for product_id, quantity in order_data.items():
                cursor.execute("SELECT Price, StockQuantity FROM Product WHERE ProductID = ?", (product_id,))
                product = cursor.fetchone()
                if not product or product[1] < quantity:
                    raise ValueError(f"Insufficient stock for ProductID {product_id}")

                price = product[0]
                total_amount += price * quantity

                #add product to OrderProduct
                cursor.execute("INSERT INTO OrderProduct (OrderID, ProductID, Quantity) VALUES (?, ?, ?)",
                               (order_id, product_id, quantity))

                #update product stock
                cursor.execute("UPDATE Product SET StockQuantity = StockQuantity - ? WHERE ProductID = ?",
                               (quantity, product_id))

            #update total amount in the order
            cursor.execute("UPDATE `Order` SET TotalAmount = ? WHERE OrderID = ?", (total_amount, order_id))
            print(f"Order Updated in DB: OrderID={order_id}, TotalAmount={total_amount}")

            cursor.execute("SELECT SupplierID FROM Supplier")
            suppliers = [row[0] for row in cursor.fetchall()]
            if not suppliers:
                raise ValueError("No suppliers available")

            supplier_id = random.choice(suppliers)

            #create a new shipment for the order
            cursor.execute(
                "INSERT INTO Shipment (OrderID, ShipmentDate, Status, SupplierID) VALUES (?, DATE('now'), 'Pending', ?)",
                (order_id, supplier_id)
            )
            shipment_id = cursor.lastrowid
            print(f"Shipment Created in DB: ShipmentID={shipment_id}, OrderID={order_id}, SupplierID={supplier_id}")

            conn.commit()
            print("Transaction committed successfully.")

            return jsonify({'message': 'Order placed successfully', 'order_id': order_id}), 200

        except ValueError as e:
            conn.rollback()
            print(f"Error: {str(e)}")
            return jsonify({'message': str(e)}), 400
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Database Error: {str(e)}")
            return jsonify({'message': 'Database error: ' + str(e)}), 500
        finally:
            conn.close()

    return jsonify({'message': 'Connection failed'}), 500

# Staff add new product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'supplier_id' not in session:
        flash('Unauthorized access! Please log in.', 'danger')
        return redirect(url_for('staff_login'))

    conn = open_connection()

    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')
        stock_quantity = request.form.get('stock_quantity')

        if not name or not price or not category or not stock_quantity:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add_product'))

        try:
            if conn:
                cursor = conn.cursor()
                sql = """
                INSERT INTO Product (Name, Price, Category, StockQuantity)
                VALUES (?, ?, ?, ?);
                """
                cursor.execute(sql, (name, price, category, stock_quantity))
                conn.commit()
                flash(f'Product "{name}" added successfully!', 'success')
            else:
                flash('Failed to connect to the database.', 'danger')
        except sqlite3.Error as e:
            conn.rollback()
            flash(f'Database error: {e}', 'danger')
        finally:
            if conn:
                conn.close()
        return redirect(url_for('mainSupplier'))

    return render_template('add_product.html')
if __name__ == '__main__':
    app.run(debug=True)