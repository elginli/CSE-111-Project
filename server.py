from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
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
            query = "SELECT * FROM Customer WHERE CustomerID = ? AND Email = ?"
            cursor.execute(query, (customer_id, email))
            user = cursor.fetchone()
            conn.close()

            if user:
                # Store the user details in the session
                session['customer_id'] = user[0]  
                session['email'] = user[2]       
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid ID or email!', 'danger')

    return render_template('login.html')  # Render the login template

    

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

# Route to get all items from Inventory
@app.route('/product', methods=['GET'])
def get_products():
    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT ProductID, Name, Price, Category, StockQuantity
                FROM Product
                WHERE StockQuantity > 0;
            """
            cursor.execute(query)
            results = cursor.fetchall()
            products = []
            for row in results:
                products.append({
                    'ProductID': row[0],  # Ensure ProductID is included
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


# Find products with price higher than 500
@app.route('/products/high-price', methods=['GET'])
def get_high_price():
    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # SQL query to fetch products priced greater than 500
            query = """
                SELECT ProductID, Name, Price, Category, StockQuantity
                FROM Product
                WHERE Price > 500
                ORDER BY Price DESC;
            """
            cursor.execute(query)
            results = cursor.fetchall()

            # Convert query results to a list of dictionaries
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


# Order products by price from cheapest
@app.route('/products/ordered-by-price', methods=['GET'])
def get_products_ordered_by_price():
    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT * 
                FROM Product
                ORDER BY Price ASC;
            """
            cursor.execute(query)
            results = cursor.fetchall()

            # Get column names for JSON keys
            column_names = [description[0] for description in cursor.description]
            ordered_products = [dict(zip(column_names, row)) for row in results]

            return jsonify(ordered_products), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()
    return jsonify({"error": "Connection failed"}), 500

#allow user to view thier order
@app.route('/my-orders', methods=['GET'])
def my_orders():
    # Ensure the user is logged in
    if 'customer_id' not in session:
        flash("You must be logged in to view your orders.")
        return redirect(url_for('login'))

    # Retrieve customer_id from session
    customer_id = session['customer_id']

    # Query the database for the logged-in customer's orders
    conn = open_connection()
    orders = []
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT 
            `Order`.OrderID AS OrderID, 
            `Order`.OrderDate AS OrderDate, 
            `Order`.TotalAmount AS TotalAmount, 
            Product.Name AS ProductName, 
            OrderProduct.Quantity AS Quantity, 
            Shipment.Status AS ShipmentStatus
        FROM `Order`
        JOIN OrderProduct ON OrderProduct.OrderID = `Order`.OrderID
        JOIN Product ON OrderProduct.ProductID = Product.ProductID
        LEFT JOIN Shipment ON `Order`.OrderID = Shipment.OrderID
        WHERE `Order`.CustomerID = ?
        ORDER BY `Order`.OrderDate DESC;
        """
        cursor.execute(query, (customer_id,))
        results = cursor.fetchall()
        conn.close()

        # Convert query results into a list of dictionaries
        for row in results:
            orders.append({
                'OrderID': row[0],
                'OrderDate': row[1],
                'TotalAmount': row[2],
                'ProductName': row[3],
                'Quantity': row[4],
                'ShipmentStatus': row[5]
            })

    # Pass the orders to the template
    return render_template('my_orders.html', orders=orders)


#get products by category
@app.route('/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # SQL query to find products by category
            query = """
                SELECT ProductID, Name, Category, Price, StockQuantity
                FROM Product
                WHERE Product.Category = ?
                ORDER BY Product.ProductID;
            """
            cursor.execute(query, (category,))
            results = cursor.fetchall()

            # Convert query results to a list of dictionaries
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

    order_data = request.json  # Receive order data as JSON
    customer_id = session['customer_id']

    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()

            # Fetch the customer's address
            cursor.execute("SELECT Address FROM Customer WHERE CustomerID = ?", (customer_id,))
            customer = cursor.fetchone()
            if not customer:
                raise ValueError("Customer not found")
            shipping_address = customer[0]

            # Create a new order
            cursor.execute(
                "INSERT INTO `Order` (OrderDate, TotalAmount, ShippingAddress, CustomerID) VALUES (DATE('now'), 0, ?, ?)",
                (shipping_address, customer_id)
            )
            order_id = cursor.lastrowid  # Get the auto-generated OrderID
            print(f"Order Created in DB: OrderID={order_id}, ShippingAddress={shipping_address}")

            total_amount = 0
            for product_id, quantity in order_data.items():
                # Fetch product details
                cursor.execute("SELECT Price, StockQuantity FROM Product WHERE ProductID = ?", (product_id,))
                product = cursor.fetchone()
                if not product or product[1] < quantity:
                    raise ValueError(f"Insufficient stock for ProductID {product_id}")

                price = product[0]
                total_amount += price * quantity

                # Add product to OrderProduct
                cursor.execute("INSERT INTO OrderProduct (OrderID, ProductID, Quantity) VALUES (?, ?, ?)",
                               (order_id, product_id, quantity))

                # Update product stock
                cursor.execute("UPDATE Product SET StockQuantity = StockQuantity - ? WHERE ProductID = ?",
                               (quantity, product_id))

            # Update total amount in the order
            cursor.execute("UPDATE `Order` SET TotalAmount = ? WHERE OrderID = ?", (total_amount, order_id))
            print(f"Order Updated in DB: OrderID={order_id}, TotalAmount={total_amount}")

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

if __name__ == '__main__':
    app.run(debug=True)