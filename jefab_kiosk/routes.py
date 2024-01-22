from jefab_kiosk import app, mysql
from flask import render_template

@app.route('/')
def index():
       cursor = mysql.connection.cursor()
       cursor.execute("SELECT * FROM products")  # Assuming 'products' is your table name
       products = cursor.fetchall()
       print(products)
       cursor.close()
       return render_template('index.html', products=products)

@app.route('/orders')
def orders():
    cursor = mysql.connection.cursor()
    sql = """
    SELECT 
        o.order_id, 
        o.date_time as order_date, 
        o.customer_contact, 
        o.total_price as order_total_price,
        p.name as product_name, 
        p.price_per_unit, 
        p.image_url, 
        oi.quantity
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    """
    cursor.execute(sql)
    orders_data = cursor.fetchall()
    cursor.close()

    formatted_orders_data = []
    for order in orders_data:
        # Format the order_date directly if it's already a datetime object
        formatted_order_date = order[1].strftime('%B %d, %Y at %I:%M:%S %p')

        # Reconstruct the order tuple with the formatted date
        formatted_order = order[:1] + (formatted_order_date,) + order[2:]
        formatted_orders_data.append(formatted_order)

    return render_template('orders.html', orders_data=formatted_orders_data)