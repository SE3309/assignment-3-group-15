DROP TABLE IF EXISTS User, Category, Address, Listing, Orders, OrderListing, Payment, Shipping, Review;

CREATE TABLE User (
    userID VARCHAR(50) NOT NULL PRIMARY KEY,
    displayName VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    phoneNo VARCHAR(15),
    email VARCHAR(100)
);

CREATE TABLE Category (
    categoryID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE Address (
    addressID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    streetAddress VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postalCode VARCHAR(20),
    country VARCHAR(100) NOT NULL
);

CREATE TABLE Listing (
    listingID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    seller VARCHAR(50) NOT NULL,
    categoryID INT NOT NULL,
    price DECIMAL(10, 2),
    description TEXT,
    addressID INT,
    images VARCHAR(255),
    FOREIGN KEY (seller) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (categoryID) REFERENCES Category(categoryID) ON DELETE CASCADE,
    FOREIGN KEY (addressID) REFERENCES Address(addressID) ON DELETE CASCADE
);

CREATE TABLE Orders (
    orderID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    buyer VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (buyer) REFERENCES User(userID) ON DELETE CASCADE
);

CREATE TABLE OrderListing (
    orderID INT NOT NULL,
    listingID INT NOT NULL,
    quantity INT DEFAULT 1,
    PRIMARY KEY (orderID, listingID),
	FOREIGN KEY (orderID) REFERENCES Orders(orderID) ON DELETE CASCADE,
    FOREIGN KEY (listingID) REFERENCES Listing(listingID) ON DELETE CASCADE
);

CREATE TABLE Payment (
    orderID INT NOT NULL PRIMARY KEY,
    paymentMethod VARCHAR(20) NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY (orderID) REFERENCES Orders(orderID) ON DELETE CASCADE
);

CREATE TABLE Shipping (
    orderID INT NOT NULL PRIMARY KEY,
    origin INT NOT NULL,
    destination INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    arrivalDate DATE,
    company VARCHAR(50),
    FOREIGN KEY (orderID) REFERENCES Orders(orderID) ON DELETE CASCADE,
    FOREIGN KEY (origin) REFERENCES Address(addressID) ON DELETE CASCADE,
    FOREIGN KEY (destination) REFERENCES Address(addressID) ON DELETE CASCADE
);

CREATE TABLE Review (
    reviewID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    userID VARCHAR(50) NOT NULL,
    orderID INT NOT NULL,
    listingID INT NOT NULL,
    rating INT NOT NULL,
    description TEXT,
    images VARCHAR(255),
    date DATE NOT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (orderID, listingID) REFERENCES OrderListing(orderID, listingID) ON DELETE CASCADE
);


DESCRIBE User;
DESCRIBE Category;
DESCRIBE Address;
DESCRIBE Listing;
DESCRIBE Orders;
DESCRIBE OrderListing;
DESCRIBE Payment;
DESCRIBE Shipping;
DESCRIBE Review;

 
 
