import streamlit as st
import pandas as pd


PROVIDERS_CSV = "C:/Local_food_Project/data/providers_data.csv"
RECEIVERS_CSV = "C:/Local_food_Project/data/receivers_data.csv"
FOOD_LISTINGS_CSV = "C:/Local_food_Project/data/food_listings_data.csv"
CLAIMS_CSV = "C:/Local_food_Project/data/claims_data.csv"


def load_data():
    providers_df = pd.read_csv(PROVIDERS_CSV)
    receivers_df = pd.read_csv(RECEIVERS_CSV)
    food_listings_df = pd.read_csv(FOOD_LISTINGS_CSV)
    claims_df = pd.read_csv(CLAIMS_CSV)
    return providers_df, receivers_df, food_listings_df, claims_df


def save_to_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        st.error(f"Error saving data to {file_path}.")
        st.exception(e)


def add_food_item(name, qty, expiry, provider_id, provider_type, city, food_type, meal_type):
    df = pd.read_csv(FOOD_LISTINGS_CSV)
    new_id = df['Food_ID'].max() + 1 if not df.empty else 1
    new_row = {
        'Food_ID': new_id,
        'Food_Name': name,
        'Quantity': qty,
        'Expiry_Date': expiry,
        'Provider_ID': provider_id,
        'Provider_Type': provider_type,
        'Location': city,
        'Food_Type': food_type,
        'Meal_Type': meal_type
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_to_csv(df, FOOD_LISTINGS_CSV)

def update_food_quantity(food_id, new_quantity):
    df = pd.read_csv(FOOD_LISTINGS_CSV)
    df.loc[df['Food_ID'] == food_id, 'Quantity'] = new_quantity
    save_to_csv(df, FOOD_LISTINGS_CSV)

def delete_food_item(food_id):
    df = pd.read_csv(FOOD_LISTINGS_CSV)
    df = df[df['Food_ID'] != food_id]
    save_to_csv(df, FOOD_LISTINGS_CSV)


def add_provider(provider_id, name, type_, city):
    df = pd.read_csv(PROVIDERS_CSV)
    new_row = {'Provider_ID': provider_id, 'Name': name, 'Type': type_, 'City': city}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_to_csv(df, PROVIDERS_CSV)

def update_provider_name(provider_id, new_name):
    df = pd.read_csv(PROVIDERS_CSV)
    df.loc[df['Provider_ID'] == provider_id, 'Name'] = new_name
    save_to_csv(df, PROVIDERS_CSV)

def delete_provider(provider_id):
    df = pd.read_csv(PROVIDERS_CSV)
    df = df[df['Provider_ID'] != provider_id]
    save_to_csv(df, PROVIDERS_CSV)


def add_receiver(receiver_id, name, organization, city):
    df = pd.read_csv(RECEIVERS_CSV)
    new_row = {'Receiver_ID': receiver_id, 'Name': name, 'Organization': organization, 'City': city}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_to_csv(df, RECEIVERS_CSV)

def update_receiver_name(receiver_id, new_name):
    df = pd.read_csv(RECEIVERS_CSV)
    df.loc[df['Receiver_ID'] == receiver_id, 'Name'] = new_name
    save_to_csv(df, RECEIVERS_CSV)

def delete_receiver(receiver_id):
    df = pd.read_csv(RECEIVERS_CSV)
    df = df[df['Receiver_ID'] != receiver_id]
    save_to_csv(df, RECEIVERS_CSV)

# Add, Update, and Delete operations for Claims
def add_claim(claim_id, food_id, receiver_id, claim_date):
    df = pd.read_csv(CLAIMS_CSV)
    new_row = {
        'Claim_ID': claim_id,
        'Food_ID': food_id,
        'Receiver_ID': receiver_id,
        'Claim_Date': claim_date,
        'Status': 'Pending'
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_to_csv(df, CLAIMS_CSV)

def update_claim_date(claim_id, new_date):
    df = pd.read_csv(CLAIMS_CSV)
    df.loc[df['Claim_ID'] == claim_id, 'Claim_Date'] = new_date
    save_to_csv(df, CLAIMS_CSV)

def delete_claim(claim_id):
    df = pd.read_csv(CLAIMS_CSV)
    df = df[df['Claim_ID'] != claim_id]
    save_to_csv(df, CLAIMS_CSV)

providers_df, receivers_df, food_listings_df, claims_df = load_data()

st.title("Local Food Wastage Management System")

operation = st.selectbox("Select Operation", ["Add", "Update", "Delete"])

if operation == "Add":
    entity_type = st.selectbox("Select Entity", ["Food", "Provider", "Receiver", "Claim"])

    if entity_type == "Food":
        food_name = st.text_input("Food Name")
        qty = st.number_input("Quantity", min_value=1)
        expiry = st.date_input("Expiry Date")
        provider_id = st.number_input("Provider ID")
        provider_type = st.text_input("Provider Type")
        city = st.text_input("City")
        food_type = st.text_input("Food Type")
        meal_type = st.text_input("Meal Type")
        if st.button("Add Food Item"):
            add_food_item(food_name, qty, expiry, provider_id, provider_type, city, food_type, meal_type)

    elif entity_type == "Provider":
        provider_id = st.number_input("Provider ID")
        provider_name = st.text_input("Provider Name")
        provider_type = st.text_input("Provider Type")
        city = st.text_input("City")
        if st.button("Add Provider"):
            add_provider(provider_id, provider_name, provider_type, city)

    elif entity_type == "Receiver":
        receiver_id = st.number_input("Receiver ID")
        receiver_name = st.text_input("Receiver Name")
        organization = st.text_input("Organization")
        city = st.text_input("City")
        if st.button("Add Receiver"):
            add_receiver(receiver_id, receiver_name, organization, city)

    elif entity_type == "Claim":
        claim_id = st.number_input("Claim ID")
        food_id = st.number_input("Food ID")
        receiver_id = st.number_input("Receiver ID")
        claim_date = st.date_input("Claim Date")
        if st.button("Add Claim"):
            add_claim(claim_id, food_id, receiver_id, claim_date)

elif operation == "Update":
    entity_type = st.selectbox("Select Entity to Update", ["Food", "Provider", "Receiver", "Claim"])
    
    if entity_type == "Food":
        food_id = st.number_input("Food ID to Update")
        new_qty = st.number_input("New Quantity")
        if st.button("Update Food Quantity"):
            update_food_quantity(food_id, new_qty)

    elif entity_type == "Provider":
        provider_id = st.number_input("Provider ID to Update")
        new_name = st.text_input("New Provider Name")
        if st.button("Update Provider Name"):
            update_provider_name(provider_id, new_name)

    elif entity_type == "Receiver":
        receiver_id = st.number_input("Receiver ID to Update")
        new_name = st.text_input("New Receiver Name")
        if st.button("Update Receiver Name"):
            update_receiver_name(receiver_id, new_name)

    elif entity_type == "Claim":
        claim_id = st.number_input("Claim ID to Update")
        new_date = st.date_input("New Claim Date")
        if st.button("Update Claim Date"):
            update_claim_date(claim_id, new_date)

elif operation == "Delete":
    entity_type = st.selectbox("Select Entity to Delete", ["Food", "Provider", "Receiver", "Claim"])

    if entity_type == "Food":
        food_id = st.number_input("Food ID to Delete")
        if st.button("Delete Food Item"):
            delete_food_item(food_id)

    elif entity_type == "Provider":
        provider_id = st.number_input("Provider ID to Delete")
        if st.button("Delete Provider"):
            delete_provider(provider_id)

    elif entity_type == "Receiver":
        receiver_id = st.number_input("Receiver ID to Delete")
        if st.button("Delete Receiver"):
            delete_receiver(receiver_id)

    elif entity_type == "Claim":
        claim_id = st.number_input("Claim ID to Delete")
        if st.button("Delete Claim"):
            delete_claim(claim_id)
