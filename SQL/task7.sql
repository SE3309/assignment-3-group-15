DROP VIEW IF EXISTS first;
DROP VIEW IF EXISTS second;

-- creating the first view
CREATE VIEW first AS
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
    Listing.price > 100.00; -- Listings priced above $100first
    
    
-- creating the second view
CREATE VIEW second AS
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
    
    
-- querying the views 
SELECT * FROM first LIMIT 5;

SELECT * FROM second LIMIT 5;

-- modifying the first view 
INSERT INTO first (buyer, displayName, orderCount) 
VALUES (999, 'Test Buyer', 5);


-- The views in this database are not updatable because they involve joins, aggregate functions, and 
-- grouping. These operations make it impossible to map changes in the view directly back to a single 
-- row in the underlying tables, which is required for a view to be updatable.



