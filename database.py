import sqlite3
import pandas as pd


conn = sqlite3.connect("food_waste.db", check_same_thread=False)
cursor = conn.cursor()

def get_providers_and_receivers_by_city():
    cursor.execute("""
        SELECT City, COUNT(*) AS Providers FROM providers GROUP BY City
        UNION ALL
        SELECT City, COUNT(*) AS Receivers FROM receivers GROUP BY City
    """)
    return cursor.fetchall()

def get_top_provider_type():
    cursor.execute("""
        SELECT Type, COUNT(*) AS Total FROM providers GROUP BY Type ORDER BY Total DESC LIMIT 1
    """)
    return cursor.fetchone()

def get_provider_contacts_by_city(city):
    cursor.execute("""
        SELECT Name, Contact FROM providers WHERE City = ?
    """, (city,))
    return cursor.fetchall()

def get_top_receivers_by_claims():
    cursor.execute("""
        SELECT r.Name, COUNT(*) AS Claims
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY c.Receiver_ID
        ORDER BY Claims DESC
    """)
    return cursor.fetchall()

def get_total_food_quantity():
    cursor.execute("SELECT SUM(Quantity) FROM food_listings")
    return cursor.fetchone()

def get_city_with_most_listings():
    cursor.execute("""
        SELECT Location, COUNT(*) AS Listings
        FROM food_listings
        GROUP BY Location
        ORDER BY Listings DESC LIMIT 1
    """)
    return cursor.fetchone()

def get_common_food_types():
    cursor.execute("""
        SELECT Food_Type, COUNT(*) AS Count
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Count DESC
    """)
    return cursor.fetchall()

def get_claims_per_food_item():
    cursor.execute("""
        SELECT f.Food_Name, COUNT(*) AS Claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY c.Food_ID
    """)
    return cursor.fetchall()

def get_provider_with_most_claims():
    cursor.execute("""
        SELECT p.Name, COUNT(*) AS Successful_Claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Provider_ID
        ORDER BY Successful_Claims DESC
        LIMIT 1;
    """)
    return cursor.fetchall()

def get_claim_status_distribution():
    cursor.execute("""
        SELECT Status AS Claim_Status, COUNT(*) AS Count
        FROM claims
        GROUP BY Status
        ORDER BY Count DESC;
    """)
    return cursor.fetchall()

def get_avg_quantity_per_receiver():
    cursor.execute("""
        SELECT AVG(Quantity)
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
    """)
    return cursor.fetchone()

def get_most_claimed_meal_type():
    cursor.execute("""
        SELECT Meal_Type, COUNT(*) AS Count
        FROM food_listings f
        JOIN claims c ON f.Food_ID = c.Food_ID
        GROUP BY Meal_Type
        ORDER BY Count DESC LIMIT 1
    """)
    return cursor.fetchone()

def get_food_quantity_by_provider():
    cursor.execute("""
        SELECT p.Name, SUM(f.Quantity) AS Total_Donated
        FROM food_listings f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY f.Provider_ID
        ORDER BY Total_Donated DESC
    """)
    return cursor.fetchall()

def get_food_claims_trend():
    cursor.execute("""
        SELECT 
    DATE(Timestamp) AS Claim_Date, 
    COUNT(*) AS Total_Claims
FROM claims
GROUP BY DATE(Timestamp)
ORDER BY Claim_Date;

    """)
    return cursor.fetchall()

def get_city_with_highest_demand():
    cursor.execute("""
        SELECT p.City, COUNT(*) AS Total_Claims
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY p.City
        ORDER BY Total_Claims DESC
        LIMIT 1;
    """)
    return cursor.fetchone()




