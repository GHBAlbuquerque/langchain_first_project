import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the database (make sure the file name matches what you created)
db_name = 'store.sqlite'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

def populate_database():
    print("Starting database population...")

    # 1. Insert Categories
    categories = ['Wellness', 'Mobile Phones', 'Audio', 'Games', 'Sports', 'Home', 'Computing', 'Electronics']
    for cat in categories:
        cursor.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", 
                       (cat, f"All products related to {cat}"))
    
    # 2. Insert Brands
    brands = [('Aurora', 'Sweden'), ('Zenit', 'Brazil'), ('Pulse', 'USA'), ('Nova', 'Canada')]
    for b_name, b_country in brands:
        cursor.execute("INSERT OR IGNORE INTO brands (name, country_of_origin) VALUES (?, ?)", 
                       (b_name, b_country))

    # 3. Insert Suppliers
    suppliers = [
        ('Global Tech Supply', 'contact@globaltech.com', '1234567890', '11111111000111', 'New York', 'NY'),
        ('BR Imports', 'import@brimports.com', '0987654321', '22222222000122', 'Sao Paulo', 'SP')
    ]
    for supp in suppliers:
        cursor.execute("INSERT OR IGNORE INTO suppliers (name, email, phone, cnpj, city, state) VALUES (?, ?, ?, ?, ?, ?)", supp)

    # Fetch IDs for relationships
    cursor.execute("SELECT id FROM categories")
    cat_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM brands")
    brand_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM suppliers")
    supp_ids = [row[0] for row in cursor.fetchall()]

    # 4. Insert Products
    print("Generating products...")
    for i in range(1, 21): # Create 20 products
        cat_id = random.choice(cat_ids)
        brand_id = random.choice(brand_ids)
        supp_id = random.choice(supp_ids)
        sku = f"SKU-{1000 + i}"
        name = f"Product Model {i}"
        cost = round(random.uniform(10.0, 300.0), 2)
        price = round(cost * random.uniform(1.3, 2.5), 2) # 30% to 150% markup
        stock = random.randint(10, 100)
        
        cursor.execute("""
            INSERT OR IGNORE INTO products (category_id, brand_id, supplier_id, sku, name, description, price, cost, stock)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cat_id, brand_id, supp_id, sku, name, f"High quality {name}", price, cost, stock))

    # 5. Insert Customers
    print("Generating customers and addresses...")
    first_names = ['John', 'Jane', 'Alice', 'Bob', 'Carlos', 'Diana']
    last_names = ['Smith', 'Doe', 'Silva', 'Johnson', 'Williams', 'Brown']
    
    for i in range(1, 11): # Create 10 customers
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"customer{i}@example.com"
        cpf = f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"
        phone = f"555-010{i}"
        
        cursor.execute("INSERT OR IGNORE INTO customers (name, email, phone, cpf) VALUES (?, ?, ?, ?)", 
                       (name, email, phone, cpf))
        
        customer_id = cursor.lastrowid
        
        if customer_id:
            # 6. Insert Address for each customer
            cursor.execute("""
                INSERT INTO addresses (customer_id, alias, street, number, city, state, zip_code, is_main)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (customer_id, 'Home', 'Main Street', str(random.randint(10, 999)), 'Metropolis', 'NY', '10001', 1))

    # 7. Insert Coupons
    cursor.execute("INSERT OR IGNORE INTO coupons (code, discount_type, discount_value) VALUES ('WELCOME10', 'percentage', 10.0)")
    cursor.execute("INSERT OR IGNORE INTO coupons (code, discount_type, discount_value) VALUES ('MINUS15', 'fixed', 15.0)")

    # 8. Generate Orders
    print("Generating orders...")
    cursor.execute("SELECT id FROM customers")
    cust_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id, price FROM products")
    products = cursor.fetchall()

    for i in range(15): # Create 15 random orders
        customer_id = random.choice(cust_ids)
        
        # Get customer address
        cursor.execute("SELECT id FROM addresses WHERE customer_id = ?", (customer_id,))
        address_row = cursor.fetchone()
        address_id = address_row[0] if address_row else None

        status = random.choice(['pending', 'paid', 'shipped', 'delivered'])
        
        cursor.execute("""
            INSERT INTO orders (customer_id, address_id, status, subtotal, discount, freight, total_amount)
            VALUES (?, ?, ?, 0, 0, 0, 0)
        """, (customer_id, address_id, status))
        
        order_id = cursor.lastrowid
        
        # Add 1 to 3 items per order
        num_items = random.randint(1, 3)
        subtotal = 0
        
        for _ in range(num_items):
            prod = random.choice(products)
            prod_id, unit_price = prod[0], prod[1]
            quantity = random.randint(1, 2)
            item_subtotal = round(unit_price * quantity, 2)
            subtotal += item_subtotal
            
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, prod_id, quantity, unit_price, item_subtotal))
            
        # Update order totals
        freight = random.choice([0.0, 15.50, 25.0])
        total_amount = subtotal + freight
        
        cursor.execute("""
            UPDATE orders SET subtotal = ?, freight = ?, total_amount = ? WHERE id = ?
        """, (subtotal, freight, total_amount, order_id))

        # 9. Generate Payments for paid/shipped/delivered orders
        if status != 'pending':
            method = random.choice(['pix', 'card', 'cash'])
            cursor.execute("""
                INSERT INTO payments (order_id, method, status, amount)
                VALUES (?, ?, 'approved', ?)
            """, (order_id, method, total_amount))

    # Commit changes
    conn.commit()
    print("Database populated successfully!")

if __name__ == '__main__':
    try:
        populate_database()
    except sqlite3.Error as error:
        print("Failed to populate database:", error)
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")