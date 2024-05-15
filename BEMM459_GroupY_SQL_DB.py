import pyodbc
# Define your SQL Server connection details
server = 'mcruebs04.isad.isadroot.ex.ac.uk'
database = 'BEMM459_GroupY'
username = 'GroupY'
password = 'XflQ315*Uh'

# Establish a connection to the SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

# Function to execute SQL queries
def execute_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

# Function to fetch data from SQL queries
def fetch_data(query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as ex:
        print(f"Error executing query: {ex}")
        return[]
    
# CRUD operations for the tables
# Create operation 

def create_customers(cus_id, cus_first_name, cus_last_name, cus_email, cus_phone_number,cus_dob,sign_up_date,cus_height,cus_weight,password,cus_diet,cus_physical_goal):
    query = f"INSERT INTO customers (cus_id, cus_first_name, cus_last_name, cus_email,cus_phone_number,cus_dob, sign_up_date,cus_height,cus_weight,password,cus_diet,cus_physical_goal) VALUES ('{cus_id}', '{cus_first_name}', '{cus_last_name}', '{cus_email}','{cus_phone_number}','{cus_dob}', '{sign_up_date}','{cus_height}','{cus_weight}','{password}', '{cus_diet}','{cus_physical_goal}')"
    execute_query(query)
    
create_customers('82702324','Richie','Rich','rich@csmonitor.com','5108398020','03-10-1958','10-18-2023','1.95','54.54','xA6/Rr)bQARc1','vegan','improve endurance')

def fetch_customer_details(cus_id):
    query = f"SELECT * FROM customers WHERE cus_id = '{cus_id}'"
    customer_details = fetch_data(query)
    
    if not customer_details:
        print(f"Customer with ID {cus_id} does not exist.")
    else:
        print("customer Details:")
        for customer in customer_details:
            print("cus_id:", customer.cus_id)
            print("cus_first_name:", customer.cus_first_name)
            print("cus_last_name:", customer.cus_last_name)
            print("cus_email:", customer.cus_email)
            print("cus_phone_number:", customer.cus_phone_number)
            print("cus_dob:", customer.cus_dob)
            print("sign_up_date:", customer.sign_up_date)
fetch_customer_details('82702324')

# Read operation example with inner join

def read_orders_with_customer_info():
    query = """
    SELECT o.*, c.cus_first_name, c.cus_last_name, c.cus_email, c.cus_phone_number
    FROM orders o
    INNER JOIN customers c ON o.cus_id = c.cus_id
    """
    rows = fetch_data(query)
    return rows
orders_with_customer_info=read_orders_with_customer_info()
#Fetching the customers who placed order

for info in orders_with_customer_info:
    print (info)

# Read operation with Left join
def read_products_with_supermarket_info():
    query = """
    SELECT p.*, sm.sm_name, sm.sm_email
    FROM products p
    LEFT JOIN super_market sm ON p.sm_id = sm.sm_id
    """
    rows = fetch_data(query)
    return rows
products_supermarket=read_products_with_supermarket_info()
for row in products_supermarket:
    print(row)

#updating the orders table
def update_order(order_id, new_purchase_date):
    query = f"UPDATE orders SET purchase_date = '{new_purchase_date}' WHERE order_id = '{order_id}'"
    execute_query(query)

update_order('v916WX00','2024-09-11')

# deleting the updated order
def delete_order(order_id):
    query = f"DELETE FROM orders WHERE order_id = '{order_id}'"
    execute_query(query)
delete_order('v916WX00')

conn.close()
