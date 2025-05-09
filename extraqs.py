import sqlite3


conn = sqlite3.connect('local_food.db', check_same_thread=False)
cursor = conn.cursor()

def get_total_providers():
    cursor.execute("SELECT COUNT(*) AS total_providers FROM providers;")
    return cursor.fetchall()

def get_total_receivers():
    cursor.execute("SELECT COUNT(*) AS total_receivers FROM receivers;")
    return cursor.fetchall()

def get_total_food_listings():
    cursor.execute("SELECT COUNT(*) AS total_listings FROM food_listings;")
    return cursor.fetchall()

def get_total_claims():
    cursor.execute("SELECT COUNT(*) AS total_claims FROM claims;")
    return cursor.fetchall()

def get_total_quantity_provided():
    cursor.execute("SELECT SUM(Quantity) AS total_quantity FROM food_listings;")
    return cursor.fetchall()

def get_food_types_available():
    cursor.execute("SELECT DISTINCT Food_Type FROM food_listings;")
    return cursor.fetchall()

def get_providers_by_location():
    cursor.execute("""
         SELECT City, COUNT(*) AS Provider_Count
        FROM providers
        GROUP BY City
        ORDER BY Provider_Count DESC;
    """)
    return cursor.fetchall()

def get_receivers_by_location():
    cursor.execute("""
       SELECT City, COUNT(*) AS Receiver_Count
        FROM receivers
        GROUP BY City
        ORDER BY Receiver_Count DESC;
    """)
    return cursor.fetchall()

def get_food_listings_by_provider():
    cursor.execute("""
        SELECT p.Name AS Provider_Name, COUNT(f.Food_ID) AS total_listings
        FROM providers p
        JOIN food_listings f ON p.Provider_ID = f.Provider_ID
        GROUP BY p.Name
        ORDER BY total_listings DESC;
    """)
    return cursor.fetchall()

def get_most_claimed_food_type():
    cursor.execute("""
        SELECT f.Food_Type, COUNT(c.Claim_ID) AS claim_count
        FROM claims c 
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Food_Type
        ORDER BY claim_count DESC
        LIMIT 1;
    """)
    return cursor.fetchall()
