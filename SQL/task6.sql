-- 1.1 Inserting a new order, linking it to an existing user and setting a specific date
INSERT INTO Orders (buyer, date)
VALUES ((SELECT userID FROM User ORDER BY userID LIMIT 1),
        '2024-11-20');
        
SET @orderID = LAST_INSERT_ID();

-- 1.2 Create new shipping and payment information for the order
INSERT INTO Shipping (orderID, origin, destination, status, arrivalDate, company)
VALUES (@orderID,
		'1',
        '2',
        'pending',
        '2024-11-26',
        'Canada Post');

INSERT INTO Payment (orderID, paymentMethod, status)
VALUES (@orderID,
		'visa',
        'pending');

-- 1.3 Adding a listing to the newly inserted order
INSERT INTO OrderListing (orderID, listingID, quantity)
VALUES (@orderID, 5, 3),  -- Insert listingID 5 with quantity of 3 for order 10
       (@orderID, 8, 2);  -- Insert listingID 8 with quantity of 2 for order 10

-- 2. Updating the shipping status of all orders that have been paid but not shipped
UPDATE Shipping
SET status = 'shipped'
WHERE orderID IN (
    SELECT orderID 
    FROM Payment 
    WHERE status = 'paid'
)
AND status = 'pending';

-- 3. Deleting orders older than a certain date along with related records
DELETE o, ol, p, s
FROM Orders o
LEFT JOIN OrderListing ol ON o.orderID = ol.orderID
LEFT JOIN Payment p ON o.orderID = p.orderID
LEFT JOIN Shipping s ON o.orderID = s.orderID
WHERE o.date < '2024-01-01';

SELECT * FROM Orders;
SELECT * FROM Payment;
SELECT * FROM Shipping;
SELECT * FROM OrderListing;