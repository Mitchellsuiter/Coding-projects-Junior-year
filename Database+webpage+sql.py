from flask import Flask
from flask import render_template, request
import pymysql

app = Flask(__name__)

# Connecting to the database
def connection():
    conn = pymysql.connect(host='host_name', user='root', password='database_password', db='nameOfDatabase')
    return conn

@app.route("/") # opens login page first because of it's just "/"s
def login():
    return render_template("login.html")

# Validate will run through the database to see what the users job title is to know what page to bring up
@app.route("/validate", methods=['POST', 'GET'])
def validate():
    if request.method == 'POST':
        uname = request.form['username']
        pswd = request.form['password']

        conn = connection()
        sql = "SELECT FirstName, LastName, EmpTitle FROM Accounts WHERE EmpUsername = %s AND EmpPassword = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (uname, pswd))
        rows = cursor.fetchall()

        print(rows[0][0]) # FirstName
        print(rows[0][1]) # LastName
        print(rows[0][2]) # EmpTitle

        if not rows:
            message = "Incorrect username or password"
            return render_template("login.html", msg=message)
        elif rows[0][2] == 'Manager':  # looks in the database for 'Manager'
            return render_template("manager.html", row=rows[0][0], rows=rows[0][1])
        elif rows[0][2] == 'Administrator':
            return render_template("admin.html", row=rows[0][0], rows=rows[0][1])
        elif rows[0][2] == 'Vendor':
            return render_template("vendor.html", row=rows[0][0], rows=rows[0][1])
        elif rows[0][2] == 'Shop Floor':
            return render_template("shop_floor.html", row=rows[0][0], rows=rows[0][1])

    return render_template("message.html", msg=":)")  # have to return some html file

# Just renders the manager"s homepage
@app.route("/manager", methods=['POST', 'GET'])
def manager():
    return render_template("manager.html")

# Renders the Admin's homepage
@app.route("/admin", methods=['POST', 'GET'])
def admin():
    return render_template("admin.html")

# Inserts information about a material in our database
@app.route("/materials_information", methods=['POST', 'GET'])
def materials_information():
    if request.method == 'POST':
        item_code = request.form['item code']
        item_name = request.form['item name']
        item_description = request.form['item description']
        price = request.form['price']
        manufacture_date = request.form['manufacture date']
        expire_date = request.form['expire date']
        manufacturer = request.form['manufacturer']
        item_image = request.form['item image']
        supplier = request.form['supplier']
        alternative_item = request.form['alternative item']

        conn = connection() # goes to the database function
        sql = "INSERT INTO MaterialInformation (ItemCode, ItemName, ItemDescription, Price, ManufactureDate, ExpireDate, " \
              "Manufacturer, ItemImage, Supplier, AlternativeItem) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(sql, (item_code, item_name, item_description, price, manufacture_date, expire_date,
                             manufacturer, item_image, supplier, alternative_item))
        conn.commit()

        message = "Item Entered!"
        return render_template("materials_information.html", msg=message)

    return render_template("materials_information.html")

# Shows a table of our material information table plus whats in our material request table combined.
@app.route('/items_table')
def items_table():
    conn = connection()

    cursor = conn.cursor()

    # This is a store procedure in the database
    cursor.execute("CALL DatabaseProject.AllItems();")

    rows = cursor.fetchall()
    return render_template("items_table.html", rows=rows)

@app.route('/search_items_table', methods=['POST', 'GET'])
def search_items_table():
    if request.method == 'POST':
        item = request.form['item']

        conn = connection()
        sql = "SELECT * FROM MaterialInformation WHERE ItemCode = %s"
        cursor = conn.cursor()
        cursor.execute(sql, item)
        rows = cursor.fetchall()

        print(rows)

        if not rows:
            message = "Item not found"
            return render_template("items_table.html", msg=message)
        elif rows:
            return render_template("items_table2.html", rows=rows)

@app.route("/deleteItem", methods=['POST', 'GET'])
def deleteItem():
    if request.method == 'POST':
        item_code = request.form['item code']

        conn = connection()
        sql = "DELETE FROM MaterialInformation WHERE ItemCode = %s"
        cursor = conn.cursor()
        cursor.execute(sql, item_code)
        conn.commit()
        rows = cursor.fetchall()

        if not rows:
            conn = connection()

            cursor = conn.cursor()
            cursor.execute("CALL DatabaseProject.AllItems();")

            rows = cursor.fetchall()
            return render_template("items_table.html", rows=rows)

@app.route("/manage_vendors", methods=['POST', 'GET'])
def manage_vendors():
    if request.method == 'POST':
        vendor_name = request.form['vendor name']
        moq = request.form['MOQ']
        dipi = request.form['date and items purchased information']
        qgs = request.form['quality of goods supplied']
        contact_details = request.form["contact details"]

        conn = connection()
        sql = "INSERT INTO Vendors (VendorsName, MOQ, OrderQuantity, SuppliedQuality, ContactDetails) " \
              "VALUES (%s, %s, %s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(sql, (vendor_name, moq, dipi, qgs, contact_details))

        conn.commit()

        message = "Vendor Added!"
        return render_template("manage_vendors.html", msg=message)

    return render_template("manage_vendors.html")

# Adds delivery schedule, order quantity, to the MaterialRequest table
@app.route ("/material_request", methods=['POST', 'GET'])
def material_request():
    if request.method == 'POST':
        item_code = request.form['item code']
        delivery_schedule = request.form['delivery schedule']
        order_quantity = request.form['order quantity']

        conn = connection ()
        sql = "INSERT INTO MaterialRequest (ItemCode, DeliverySchedule, OrderQuantity) VALUES (%s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(sql, (item_code, delivery_schedule, order_quantity))

        conn.commit()

        message = "Item Details Added!"
        return render_template("material_request.html", msg=message)

    return render_template("material_request.html")

@app.route("/order", methods=['POST', 'GET'])
def order():
    return render_template("order.html")

@app.route("/item_quantity", methods=['POST', 'GET'])
def item_quantity():
    if request.method == 'POST':
        item = request.form['item code']

        conn = connection()
        sql = "SELECT MaterialInformation.ItemCode, MaterialRequest.OrderQuantity FROM MaterialInformation " \
              "INNER JOIN MaterialRequest ON MaterialInformation.ItemCode = MaterialRequest.ItemCode " \
              "WHERE MaterialInformation.ItemCode = %s"
        cursor = conn.cursor()
        cursor.execute(sql, item)
        rows = cursor.fetchall()

        if not rows:
            message = "Item not found"
            return render_template("order.html", msg=message)
        elif rows:
            message = "Item Found!"
            return render_template("item_quantity.html", msg=message, rows=rows, row=rows[0][0]) #the last row will return the ItemCode

    return render_template("message.html", msg=":)")

@app.route("/make_purchase_order", methods=['POST', 'GET'])
def make_purchase_order():
    if request.method == 'POST':
        item1 = request.form['item1']
        quantity1 = request.form['quantity1']

        conn = connection()
        sql = "UPDATE MaterialRequest SET OrderQuantity = (OrderQuantity) - %s WHERE ItemCode = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (quantity1, item1))
        conn.commit() # Need to have commit() to save the update in the database
        rows = cursor.fetchall()

        message = "Purchase Order Completed!"
        return render_template("order.html", msg=message)


    return render_template("make_purchase_order.html", msg=":)")

@app.route("/manage_accounts", methods=['POST', 'GET'])
def manage_accounts():
    if request.method == 'POST':
        first_name = request.form['first name']
        last_name = request.form['last name']
        gender = request.form['gender']
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone number']
        email = request.form['email']
        home_address = request.form['home address']
        job_title = request.form['title']

        conn = connection()  # goes to the database function
        sql = "INSERT INTO Accounts (FirstName, LastName, Gender, EmpUsername, EmpPassword, PhoneNumber, " \
              "EmailAddress, HomeAddress, EmpTitle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(sql, (first_name, last_name, gender, username, password, phone_number,
                              email, home_address, job_title))

        conn.commit()

        message = "Account Added!"
        return render_template("manage_accounts.html", msg=message)

    return render_template("manage_accounts.html")

@app.route("/all_accounts", methods=['POST', 'GET'])
def all_accounts():
    conn = connection()

    cursor = conn.cursor()

    # This is a stored procedure
    cursor.execute("CALL DatabaseProject.All_Accounts();")

    rows = cursor.fetchall()
    return render_template("all_accounts.html", rows=rows)

@app.route("/deleteAccount", methods=['POST', 'GET'])
def deleteAccount():
    if request.method == 'POST':
        username = request.form['username']

        conn = connection()
        sql = "DELETE FROM Accounts WHERE EmpUsername = %s"
        cursor = conn.cursor()
        cursor.execute(sql, username)
        conn.commit()
        rows = cursor.fetchall()

        if not rows:
            conn = connection()

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Accounts")

            rows = cursor.fetchall()
            return render_template("all_accounts.html", rows=rows)

@app.route("/shipping_details", methods=['POST', 'GET'])
def shipping_details():
    if request.method == 'POST':
        shipping_address = request.form['shipping address']
        contact_info = request.form['contact information']
        payment_method = request.form['payment method']

        conn = connection()
        sql = "INSERT INTO ShippingDetails (ShippingAddress, ContactInformation, PaymentMethod) VALUES (%s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(sql, (shipping_address, contact_info, payment_method))

        conn.commit()
    return render_template("shipping_details.html")

@app.route("/vendor", methods=['POST', 'GET'])
def vendor():
    return render_template("vendor.html")

@app.route("/supply_materials", methods=['POST', 'GET'])
def supply_materials():
    return render_template("supply_materials.html")

@app.route("/send_receipt", methods=['POST', 'GET'])
def send_receipt():
    return render_template("send_receipt.html")

if __name__ == "__main__":
    app.run(debug=True)

# If I need to kill the address that is running in the background
# lsof -n -i4TCP:5000
#kill -9 23559
#etc