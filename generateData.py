import mysql.connector
from faker import Faker
import random
import logging
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Configure logging
logging.basicConfig(filename='data_generation.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

# Connect to the MySQL database
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Change to your MySQL username
        password='1@Kirill360',  # Change to your MySQL password
        database='MyDatabase'  # Ensure this matches your database name
    )
    cursor = conn.cursor()
except mysql.connector.Error as e:
    logging.error(f"Error connecting to the database: {e}")
    exit(1)

# Function to generate fake data for User table
def generate_fake_user_data(num_records):
    user_ids = []
    for _ in range(num_records):
        userID = fake.unique.random_int(min=1, max=1000)  # Unique userID
        displayName = fake.name()[:50]
        password = fake.password()[:255]
        role = fake.random_element(elements=('admin', 'user', 'guest'))[:20]
        phoneNo = fake.phone_number()[:15]
        email = fake.email()[:100]

        try:
            cursor.execute('''
                INSERT INTO User (userID, displayName, password, role, phoneNo, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (userID, displayName, password, role, phoneNo, email))
            user_ids.append(userID)
        except mysql.connector.Error as e:
            logging.error(f"Error inserting data into User table: {e}, Query: {cursor.statement}")
            continue

    return user_ids

# Function to generate fake data for Category table
def generate_fake_category_data(num_records):
    category_ids = []
    for _ in range(num_records):
        name = fake.word()[:50]

        try:
            cursor.execute('''
                INSERT INTO Category (name)
                VALUES (%s)
            ''', (name,))
            category_ids.append(cursor.lastrowid)
        except mysql.connector.Error as e:
            logging.error(f"Error inserting data into Category table: {e}, Query: {cursor.statement}")
            continue

    return category_ids

# Function to generate fake data for Address table
def generate_fake_address_data(num_records):
    address_ids = []
    for _ in range(num_records):
        streetAddress = fake.street_address()[:255]
        city = fake.city()[:100]
        state = fake.state()[:100]
        postalCode = fake.postcode()[:20]
        country = fake.country()[:100]

        try:
            cursor.execute('''
                INSERT INTO Address (streetAddress, city, state, postalCode, country)
                VALUES (%s, %s, %s, %s, %s)
            ''', (streetAddress, city, state, postalCode, country))
            address_ids.append(cursor.lastrowid)
        except mysql.connector.Error as e:
            logging.error(f"Error inserting data into Address table: {e}, Query: {cursor.statement}")
            continue

    return address_ids

# Function to generate fake data for Listing table
def generate_fake_listing_data(num_records, user_ids, category_ids, address_ids):
    listing_ids = []
    for _ in range(num_records):
        seller = random.choice(user_ids)
        categoryID = random.choice(category_ids)
        price = round(random.uniform(10.0, 1000.0), 2)
        description = fake.text()[:1000]
        addressID = random.choice(address_ids)
        images = ','.join([fake.image_url() for _ in range(random.randint(1, 5))])[:255]

        try:
            cursor.execute('''
                INSERT INTO Listing (seller, categoryID, price, description, addressID, images)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (seller, categoryID, price, description, addressID, images))
            listing_ids.append(cursor.lastrowid)
        except mysql.connector.Error as e:
            logging.error(f"Error inserting data into Listing table: {e}, Query: {cursor.statement}")
            continue

    return listing_ids

# Function to generate fake data for Orders table
def generate_fake_order_data(num_records, user_ids):
    order_ids = []
    for _ in range(num_records):
        buyer = random.choice(user_ids)
        date = fake.date_between(start_date='-1y', end_date='today')

        try:
            cursor.execute('''
                INSERT INTO Orders (buyer, date)
                VALUES (%s, %s)
            ''', (buyer, date))
            order_ids.append(cursor.lastrowid)
        except mysql.connector.Error as e:
            logging.error(f"Error inserting data into Orders table: {e}, Query: {cursor.statement}")
            continue

    return order_ids

# Function to generate fake data for OrderListing table
def generate_fake_order_listing_data(num_records, order_ids, listing_ids):
    order_listing_pairs = []
    for _ in range(num_records):
        orderID = random.choice(order_ids)
        listingID = random.choice(listing_ids)
        quantity = random.randint(1, 5)

        try:
            cursor.execute('''
                INSERT INTO OrderListing (orderID, listingID, quantity)
                VALUES (%s, %s, %s)
            ''', (orderID, listingID, quantity))
            order_listing_pairs.append((orderID, listingID))
        except mysql.connector.Error as e:
            logging.error(f"Error inserting data into OrderListing table: {e}, Query: {cursor.statement}")
            continue

    return order_listing_pairs

# Function to generate fake data for Payment table
def generate_fake_payment_data(order_ids):
    for orderID in order_ids:
        paymentMethod = fake.random_element(elements=('credit_card', 'paypal', 'bank_transfer', 'cash'))[:20]
        status = fake.random_element(elements=('completed', 'pending', 'failed'))[:10]

        try:
            cursor.execute('''
                INSERT INTO Payment (orderID, paymentMethod, status)
                VALUES (%s, %s, %s)
            ''', (orderID, paymentMethod, status))
        except mysql.connector.Error as e:
            logging.error(f"Error inserting data into Payment table: {e}, Query: {cursor.statement}")
            continue

# Function to generate fake data for Shipping table
def generate_fake_shipping_data(order_ids, address_ids):
    for orderID in order_ids:
        origin = random.choice(address_ids)
        destination = random.choice(address_ids)
        while origin == destination:
            destination = random.choice(address_ids)
        status = fake.random_element(elements=('shipped', 'in_transit', 'delivered', 'cancelled'))[:20]
        arrivalDate = fake.date_between(start_date='-1y', end_date='+30d') if status == 'delivered' else None
        company = fake.company()[:50]

        try:
            cursor.execute('''
                INSERT INTO Shipping (orderID, origin, destination, status, arrivalDate, company)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (orderID, origin, destination, status, arrivalDate, company))
        except mysql.connector.Error as e:
            logging.error(f"Error inserting data into Shipping table: {e}, Query: {cursor.statement}")
            continue

# Function to generate fake data for Review table
def generate_fake_review_data(num_records, user_ids, order_listing_pairs):
    for _ in range(num_records):
        userID = random.choice(user_ids)
        orderID, listingID = random.choice(order_listing_pairs)
        rating = random.randint(1, 5)
        description = fake.text()[:1000]
        images = ','.join([fake.image_url() for _ in range(random.randint(1, 3))])[:255]
        date = fake.date_between(start_date='-1y', end_date='today')

        try:
            cursor.execute('''
                INSERT INTO Review (userID, orderID, listingID, rating, description, images, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (userID, orderID, listingID, rating, description, images, date))
        except mysql.connector.Error as e:
            logging.error(f"Error inserting data into Review table: {e}, Query: {cursor.statement}")
            continue

# Main script
user_ids = generate_fake_user_data(100)
category_ids = generate_fake_category_data(50)
address_ids = generate_fake_address_data(100)
listing_ids = generate_fake_listing_data(200, user_ids, category_ids, address_ids)
order_ids = generate_fake_order_data(100, user_ids)
order_listing_pairs = generate_fake_order_listing_data(300, order_ids, listing_ids)
generate_fake_payment_data(order_ids)
generate_fake_shipping_data(order_ids, address_ids)
generate_fake_review_data(200, user_ids, order_listing_pairs)

# Commit and close
try:
    conn.commit()
except mysql.connector.Error as e:
    logging.error(f"Error committing changes: {e}")
finally:
    cursor.close()
    conn.close()

print("Fake data generated successfully!")
