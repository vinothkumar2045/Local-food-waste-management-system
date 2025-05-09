import sqlite3
import pandas as pd


conn = sqlite3.connect("food_waste.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    Address TEXT,
    City TEXT,
    Contact TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS receivers (
    Receiver_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    City TEXT,
    Contact TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS food_listings (
    Food_ID INTEGER PRIMARY KEY,
    Food_Name TEXT,
    Quantity INTEGER,
    Expiry_Date TEXT,
    Provider_ID INTEGER,
    Provider_Type TEXT,
    Location TEXT,
    Food_Type TEXT,
    Meal_Type TEXT,
    FOREIGN KEY (Provider_ID) REFERENCES providers (Provider_ID)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS claims (
    Claim_ID INTEGER PRIMARY KEY,
    Food_ID INTEGER,
    Receiver_ID INTEGER,
    Status TEXT,
    Timestamp TEXT,
    FOREIGN KEY (Food_ID) REFERENCES food_listings (Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers (Receiver_ID)
)
""")


conn.commit()


providers_df = pd.read_csv("C:/Local_food_Project/data/providers_data.csv")
receivers_df = pd.read_csv("C:/Local_food_Project/data/receivers_data.csv")
food_listings_df = pd.read_csv("C:/Local_food_Project/data/food_listings_data.csv")
claims_df = pd.read_csv("C:/Local_food_Project/data/claims_data.csv")


providers_df.to_sql("providers", conn, if_exists="append", index=False)
receivers_df.to_sql("receivers", conn, if_exists="append", index=False)
food_listings_df.to_sql("food_listings", conn, if_exists="append", index=False)
claims_df.to_sql("claims", conn, if_exists="append", index=False)


conn.commit()
conn.close()

print("✅ Database and tables created successfully and data inserted.")
