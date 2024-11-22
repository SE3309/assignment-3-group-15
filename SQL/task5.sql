/*1. Query to List All Listings with Descriptions and Their Seller's Display Name and Category Name*/
SELECT 
    Listing.listingID,
    Listing.description,
    User.displayName AS sellerName,
    Category.name AS categoryName
FROM 
    Listing
JOIN 
    User ON Listing.seller = User.userID
JOIN 
    Category ON Listing.categoryID = Category.categoryID
WHERE 
    Listing.price > 100.00; -- Listings priced above $100


/*2. Query to Find Buyers with More Than 2 Orders*/ 
SELECT 
    Orders.buyer, 
    User.displayName, 
    COUNT(*) AS orderCount
FROM 
    Orders
JOIN 
    User ON Orders.buyer = User.userID
GROUP BY 
    Orders.buyer, User.displayName
HAVING 
    COUNT(*) > 2;

/*3. Query to Find the Most Expensive Listing in Each Category*/
SELECT 
    Category.name AS categoryName,
    Listing.listingID,
    Listing.description,
    MAX(Listing.price) AS highestPrice
FROM 
    Listing
JOIN 
    Category ON Listing.categoryID = Category.categoryID
GROUP BY 
    Category.name, Listing.listingID, Listing.description
ORDER BY 
    highestPrice DESC;


/*4. Query to Retrieve Listings that Have Never Been Ordered*/
SELECT 
    Listing.listingID, 
    Listing.description
FROM 
    Listing
WHERE 
    NOT EXISTS (
        SELECT 
            1 
        FROM 
            OrderListing 
        WHERE 
            OrderListing.listingID = Listing.listingID
    );

/*5. List all users who have not placed any orders*/
SELECT *
FROM User U
WHERE NOT EXISTS (
    SELECT 1
    FROM Orders O
    WHERE O.buyer = U.userID
);

/*6. Query to List the Average Rating for Each Seller's Listings*/
SELECT 
    User.displayName AS sellerName,
    AVG(Review.rating) AS averageRating
FROM 
    Review
JOIN 
    Listing ON Review.listingID = Listing.listingID
JOIN 
    User ON Listing.seller = User.userID
GROUP BY 
    User.displayName
HAVING 
    AVG(Review.rating) > 3; -- Only sellers with an average rating above 3

/*7. Query to Find All Orders Shipped by a Specific Company with Destination in a Specific City*/
SELECT 
    Orders.orderID,
    Shipping.company,
    Address.city AS destinationCity,
    Shipping.status,
    Shipping.arrivalDate
FROM 
    Orders
JOIN 
    Shipping ON Orders.orderID = Shipping.orderID
JOIN 
    Address ON Shipping.destination = Address.addressID
WHERE 
    Shipping.company = 'Mason PLC' -- Specify the shipping company
    AND Address.city = 'North Brianbury'; -- Specify the destination city
