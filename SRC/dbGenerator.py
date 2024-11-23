import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Connect to the MySQL database
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Change to your MySQL username (found running 'SELECT USER()' in MySQL, everything before the @ symbol is the username)
        password='Password',  # Change to your MySQL password
        database='myDB'  # Ensure this matches your database name
    )
    cursor = conn.cursor()
except mysql.connector.Error as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# Function to generate fake data for User table
def generate_fake_user_data(num_records):
    user_ids = []
    for _ in range(num_records):
        userID = fake.unique.user_name()[:50]  # Unique userID
        displayName = fake.name()[:50]  # Truncate to 50 characters
        password = fake.password()[:255]  # Truncate to 255 characters
        role = fake.random_element(elements=('admin', 'user', 'guest'))[:20]  # Truncate to 20 characters
        phoneNo = fake.phone_number()[:15]  # Truncate to 15 characters
        email = fake.email()[:100]  # Truncate to 100 characters

        try:
            cursor.execute('''
                INSERT INTO User (userID, displayName, password, role, phoneNo, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (userID, displayName, password, role, phoneNo, email))
            user_ids.append(userID)
        except mysql.connector.Error as e:
            print(f"Error inserting data into User table: {e}")
            continue
    return user_ids

# Function to generate fake data for Category table
def generate_fake_category_data(num_records):
    for _ in range(num_records):
        name = fake.word()[:50]  # Truncate to 50 characters

        try:
            cursor.execute('''
                INSERT INTO Category (name)
                VALUES (%s)
            ''', (name,))
        except mysql.connector.Error as e:
            print(f"Error inserting data into Category table: {e}")
            continue

# Function to generate fake data for Address table
def generate_fake_address_data(num_records):
    for _ in range(num_records):
        streetAddress = fake.street_address()[:255]  # Truncate to 255 characters
        city = fake.city()[:100]  # Truncate to 100 characters
        state = fake.state()[:100]  # Truncate to 100 characters
        postalCode = fake.postcode()[:20]  # Truncate to 20 characters
        country = fake.country()[:100]  # Truncate to 100 characters

        try:
            cursor.execute('''
                INSERT INTO Address (streetAddress, city, state, postalCode, country)
                VALUES (%s, %s, %s, %s, %s)
            ''', (streetAddress, city, state, postalCode, country))
        except mysql.connector.Error as e:
            print(f"Error inserting data into Address table: {e}")
            continue

# Function to generate fake data for Listing table
def generate_fake_listing_data(num_records, user_ids, category_ids, address_ids):
    for _ in range(num_records):
        seller = random.choice(user_ids)
        categoryID = random.randint(1, category_ids)
        price = round(random.uniform(10.0, 1000.0), 2)
        description = fake.text()[:1000]  # Truncate to 1000 characters
        addressID = random.randint(1, address_ids)
        images = ','.join([fake.image_url() for _ in range(random.randint(1, 5))])[:255]  # Truncate to 255 characters

        try:
            cursor.execute('''
                INSERT INTO Listing (seller, categoryID, price, description, addressID, images)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (seller, categoryID, price, description, addressID, images))
        except mysql.connector.Error as e:
            print(f"Error inserting data into Listing table: {e}")
            continue

# Function to generate fake data for Orders table
def generate_fake_order_data(num_records, user_ids):
    for _ in range(num_records):
        buyer = random.choice(user_ids)
        date = fake.date_between(start_date='-1y', end_date='today')

        try:
            cursor.execute('''
                INSERT INTO Orders (buyer, date)
                VALUES (%s, %s)
            ''', (buyer, date))
        except mysql.connector.Error as e:
            print(f"Error inserting data into Orders table: {e}")
            continue

# Function to generate fake data for OrderListing table
def generate_fake_order_listing_data(num_records, order_ids, listing_ids):
    used_combinations = set()
    order_listing_pairs = []
    
    for _ in range(num_records):
        orderID = random.randint(1, order_ids)
        listingID = random.randint(1, listing_ids)
        quantity = random.randint(1, 10)
        
        while (orderID, listingID) in used_combinations:
            orderID = random.randint(1, order_ids)
            listingID = random.randint(1, listing_ids)
        
        used_combinations.add((orderID, listingID))
        order_listing_pairs.append((orderID, listingID))

        try:
            cursor.execute('''
                INSERT INTO OrderListing (orderID, listingID, quantity)
                VALUES (%s, %s, %s)
            ''', (orderID, listingID, quantity))
        except mysql.connector.Error as e:
            print(f"Error inserting data into OrderListing table: {e}")
            continue
    return order_listing_pairs

# Function to generate fake data for Review table
def generate_fake_review_data(num_records, user_ids, order_listing_pairs):
    for _ in range(num_records):
        userID = random.choice(user_ids)
        orderID, listingID = random.choice(order_listing_pairs)
        rating = random.randint(1, 5)
        description = fake.text()[:1000]  # Truncate to 1000 characters
        images = ','.join([fake.image_url() for _ in range(random.randint(1, 5))])[:255]  # Truncate to 255 characters
        date = fake.date_between(start_date='-1y', end_date='today')

        try:
            cursor.execute('''
                INSERT INTO Review (userID, orderID, listingID, rating, description, images, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (userID, orderID, listingID, rating, description, images, date))
        except mysql.connector.Error as e:
            print(f"Error inserting data into Review table: {e}")
            continue

# Function to generate fake data for Payment table
def generate_fake_payment_data(num_records, order_ids):
    for _ in range(num_records):
        orderID = _ + 1
        paymentMethod = fake.random_element(elements=('credit_card', 'paypal', 'bank_transfer'))[:20]  # Truncate to 20 characters
        status = fake.random_element(elements=('pending', 'paid', 'failed'))[:10]  # Truncate to 10 characters

        try:
            cursor.execute('''
                INSERT INTO Payment (orderID, paymentMethod, status)
                VALUES (%s, %s, %s)
            ''', (orderID, paymentMethod, status))
        except mysql.connector.Error as e:
            print(f"Error inserting data into Payment table: {e}")
            continue

# Function to generate fake data for Shipping table
def generate_fake_shipping_data(num_records, order_ids, address_ids):
    for _ in range(num_records):
        orderID = _ + 1
        origin = random.randint(1, address_ids)
        destination = random.randint(1, address_ids)
        status = fake.random_element(elements=('pending', 'shipped', 'delivered', 'returned'))[:20]  # Truncate to 20 characters
        arrivalDate = fake.date_between(start_date='+1d', end_date='+1w')
        company = fake.company()[:50]  # Truncate to 50 characters

        try:
            cursor.execute('''
                INSERT INTO Shipping (orderID, origin, destination, status, arrivalDate, company)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (orderID, origin, destination, status, arrivalDate, company))
        except mysql.connector.Error as e:
            print(f"Error inserting data into Shipping table: {e}")
            continue

# Generate a number of fake records for all tables
user_ids = generate_fake_user_data(300) #the number determines how many to generate
category_ids = 50
generate_fake_category_data(category_ids)
address_ids = 300
generate_fake_address_data(address_ids)
listing_ids = 500
generate_fake_listing_data(listing_ids, user_ids, category_ids, address_ids)
order_ids = 1000
generate_fake_order_data(order_ids, user_ids)
order_listing_pairs = generate_fake_order_listing_data(3000, order_ids, listing_ids)
generate_fake_review_data(300, user_ids, order_listing_pairs)
generate_fake_payment_data(1000, order_ids)
generate_fake_shipping_data(1000, order_ids, address_ids)

# Commit changes and close the connection
try:
    conn.commit()
except mysql.connector.Error as e:
    print(f"Error committing changes: {e}")

cursor.close()
conn.close()

print("Fake data generated successfully!")
#if the above print statement prints then the data has been generated
#Check the MySQL table to see the generated data!

