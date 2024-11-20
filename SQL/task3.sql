-- Delete statements to delete existing records so I can keep running the statements to debug
DELETE FROM Listing WHERE seller IN (1, 2);
DELETE FROM User WHERE userID IN (1, 2);
DELETE FROM Address WHERE addressID IN (1, 2);
DELETE FROM Category WHERE categoryID IN (1, 2);

-- Other simple inserts for the foreign key constraints
INSERT INTO Address VALUES (1, '1915 Western Avenue', 'London', 'Ontario', 'N5X8N7', 'Canada');
INSERT INTO Address VALUES (2, '18 North Road', 'New York', 'New York State', '10009', 'United States of America');
INSERT INTO Category VALUES( 1, 'Electronics');
INSERT INTO Category VALUES (2, 'Sports');
INSERT INTO User VALUES (1, 'hkim946', '1234password', 'Seller', '2263428593', 'harrykim@gmail.com');
INSERT INTO User VALUES (2, 'seller123', 'password0000', 'Seller', '4832022423', 'sellingman23@outlook.com');

    
-- First insert statement   
INSERT INTO Listing VALUES
(
	1,
    1,
    1,
    '295.95',
    'Brand new Playstation 5',
    5,
    'ps5_image.jpg'
    );
	
-- Second Insert Statement
INSERT INTO Listing (
	listingID,
    seller,
    categoryID,
    price,
    description,
    addressID,
    images
) VALUES (
		2,
        1,
        (SELECT categoryID FROM Category WHERE name = 'Electronics' LIMIT 1),
        599.99,
        'Used, almost new iPhone 15',
        (SELECT AddressID FROM Address WHERE streetAddress = '1915 Western Avenue'LIMIT 1),
        'phone_pic.jpg'
        );

-- Third insert statement
INSERT INTO Listing (listingID, seller, categoryID, price, description, addressID, images)
SELECT 3, 2, 2, 249.99, 'Used Bicycle in excellent condition', addressID, 'bicycle_image.jpg'
FROM Category, Address
WHERE Category.name = 'Sports' AND Address.city = 'New York' LIMIT 1;


-- Select statement for Listing table
SELECT *
FROM Listing
WHERE listingID IS NOT NULL;          

 
        
