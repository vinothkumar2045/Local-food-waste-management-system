import streamlit as st
import pandas as pd
import sqlite3
from database import (
    get_total_food_quantity,
    get_providers_and_receivers_by_city,
    get_top_provider_type,
    get_provider_contacts_by_city,
    get_top_receivers_by_claims,
    get_city_with_most_listings,
    get_common_food_types,
    get_claims_per_food_item,
    get_provider_with_most_claims,
    get_claim_status_distribution,
    get_avg_quantity_per_receiver,
    get_most_claimed_meal_type,
    get_food_quantity_by_provider,
    get_food_claims_trend,
    get_city_with_highest_demand
)
from extraqs import (
    get_total_providers,
    get_total_receivers,
    get_total_food_listings,
    get_total_claims,
    get_total_quantity_provided,
    get_food_types_available,
    get_providers_by_location,
    get_receivers_by_location,
    get_food_listings_by_provider,
    get_most_claimed_food_type
)   
from CRUD_CSV import (
    add_food_item, update_food_quantity, delete_food_item,
    add_provider, update_provider_name, delete_provider,
    add_receiver, update_receiver_name, delete_receiver,
    add_claim, update_claim_date, delete_claim
)

try:
    providers_df = pd.read_csv("C:/Local_food_Project/data/providers_data.csv")
    receivers_df = pd.read_csv("C:/Local_food_Project/data/receivers_data.csv")
    food_listings_df = pd.read_csv("C:/Local_food_Project/data/food_listings_data.csv")
    claims_df = pd.read_csv("C:/Local_food_Project/data/claims_data.csv")
except FileNotFoundError as e:
    st.error("Error loading CSV files. Please ensure the paths are correct.")
    st.exception(e)
except pd.errors.EmptyDataError as e:
    st.error("Error: One or more CSV files are empty.")
    st.exception(e)
except Exception as e:
    st.error("An unexpected error occurred while loading the data.")
    st.exception(e)
    



conn = sqlite3.connect("local_food.db")  
cursor = conn.cursor()


providers_df.to_sql('providers', conn, if_exists='replace', index=False)
receivers_df.to_sql('receivers', conn, if_exists='replace', index=False)
food_listings_df.to_sql('food_listings', conn, if_exists='replace', index=False)
claims_df.to_sql('claims', conn, if_exists='replace', index=False)


st.set_page_config(page_title="Local Food Wastage Management", layout="wide")


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Project Introduction",
    "View Tables",
    "CRUD Operations",
    "SQL Queries & Visualization",
    "Learner SQL Queries",
    "User Introduction"
])


if page == "Project Introduction":
    st.title("🍛 Local Food Wastage Management System")
    st.write("""
        Welcome to the **Local Food Wastage Management System**, a project dedicated to tackling one of 
        the world's most pressing issues – food waste.

        ## Objective:
        The goal of this project is to efficiently manage excess food donations from local providers and 
        distribute it to receivers in need. The system ensures that food is not wasted, and instead, it is 
        put to good use in alleviating hunger and supporting local communities.

        ## Key Features:
        - **Food Listings**: The system tracks the available food items, including details such as food name, 
          quantity, expiry date, and provider information.
        - **Food Claims**: Receivers can claim food, and the system helps monitor the status of claims.
        - **Data Visualizations**: The system includes various data visualizations to track trends in food donations, 
          claims, and quantities provided, helping stakeholders make informed decisions.
        - **Efficient Matching**: Providers and receivers are matched based on location, food types, and availability, 
          ensuring that food donations reach those who need them most.

        ## How It Works:
        1. **Providers** input details about the excess food they have available, including quantities and expiry dates.
        2. **Receivers** can browse the available food listings and claim items.
        3. The system tracks all claims, and once the food is claimed, it is removed from the listings.
        4. Data is analyzed to generate reports and trends on food wastage and donations.

        ## Social Impact:
        This system not only helps reduce food waste but also contributes to addressing hunger and food insecurity 
        in local communities. By providing a platform for donations and claims, we make it easier for everyone to 
        play their part in creating a sustainable, waste-free world.

        Thank you for being a part of this project to make a positive change in the community!
    """)


elif page == "View Tables":
    st.title("📑 View Tables")
    

    table_choice = st.selectbox("Select a table to view:", [
        "Providers", "Receivers", "Food Listings", "Claims"
    ])
    
  
    if table_choice == "Providers":
        df = providers_df
    elif table_choice == "Receivers":
        df = receivers_df
    elif table_choice == "Food Listings":
        df = food_listings_df
    elif table_choice == "Claims":
        df = claims_df
    
    st.subheader(f"{table_choice} Table")
    st.dataframe(df)


elif page == "CRUD Operations":
    st.title("Manage Data")
    table = st.selectbox("Select Table", ["Food", "Provider", "Receiver", "Claim"])
    action = st.selectbox("Choose an Action", ["Add", "Update", "Delete"])

    
    if table == "Food":
        try:
            if action == "Add":
                st.subheader("➕ Add New Food Item")
                with st.form("add_food"):
                    name = st.text_input("Food Name")
                    qty = st.number_input("Quantity", min_value=1)
                    expiry = st.date_input("Expiry Date")
                    provider_id = st.number_input("Provider ID", min_value=1)
                    provider_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket"])
                    city = st.text_input("City")
                    food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
                    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
                    submitted = st.form_submit_button("Add Food")

                if submitted:
                    add_food_item(name, qty, expiry, provider_id, provider_type, city, food_type, meal_type)
                    st.success("Food item added successfully!")

            elif action == "Update":
                st.subheader("✏️ Update Food Quantity")
                food_id = st.number_input("Food ID to Update", min_value=1)
                new_quantity = st.number_input("New Quantity", min_value=1)
                if st.button("Update Food"):
                    update_food_quantity(food_id, new_quantity)
                    st.success(f"Food ID {food_id} updated successfully!")

            elif action == "Delete":
                st.subheader("🗑️ Delete Food Item")
                food_id = st.number_input("Food ID to Delete", min_value=1)
                if st.button("Delete Food"):
                    delete_food_item(food_id)
                    st.warning(f"Food ID {food_id} deleted.")
        except Exception as e:
            st.error("An error occurred while performing the CRUD operation.")
            st.exception(e)

    
    elif table == "Provider":
        try:
            if action == "Add":
                st.subheader("➕ Add New Provider")
                with st.form("add_provider"):
                    provider_id = st.number_input("Provider ID", min_value=1)
                    name = st.text_input("Provider Name")
                    type_ = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket"])
                    city = st.text_input("City")
                    submitted = st.form_submit_button("Add Provider")
                if submitted:
                    add_provider(provider_id, name, type_, city)
                    st.success("Provider added successfully!")

            elif action == "Update":
                st.subheader("✏️ Update Provider Name")
                provider_id = st.number_input("Provider ID to Update", min_value=1)
                new_name = st.text_input("New Provider Name")
                if st.button("Update Provider"):
                    update_provider_name(provider_id, new_name)
                    st.success(f"Provider ID {provider_id} updated.")

            elif action == "Delete":
                st.subheader("🗑️ Delete Provider")
                provider_id = st.number_input("Provider ID to Delete", min_value=1)
                if st.button("Delete Provider"):
                    delete_provider(provider_id)
                    st.warning(f"Provider ID {provider_id} deleted.")
        except Exception as e:
            st.error("An error occurred while performing the CRUD operation.")
            st.exception(e)

    
    elif table == "Receiver":
        try:
            if action == "Add":
                st.subheader("➕ Add New Receiver")
                with st.form("add_receiver"):
                    receiver_id = st.number_input("Receiver ID", min_value=1)
                    name = st.text_input("Receiver Name")
                    organization = st.text_input("Organization")
                    city = st.text_input("City")
                    submitted = st.form_submit_button("Add Receiver")
                if submitted:
                    add_receiver(receiver_id, name, organization, city)
                    st.success("Receiver added successfully!")

            elif action == "Update":
                st.subheader("✏️ Update Receiver Name")
                receiver_id = st.number_input("Receiver ID to Update", min_value=1)
                new_name = st.text_input("New Receiver Name")
                if st.button("Update Receiver"):
                    update_receiver_name(receiver_id, new_name)
                    st.success(f"Receiver ID {receiver_id} updated.")

            elif action == "Delete":
                st.subheader("🗑️ Delete Receiver")
                receiver_id = st.number_input("Receiver ID to Delete", min_value=1)
                if st.button("Delete Receiver"):
                    delete_receiver(receiver_id)
                    st.warning(f"Receiver ID {receiver_id} deleted.")
        except Exception as e:
            st.error("An error occurred while performing the CRUD operation.")
            st.exception(e)

    
    elif table == "Claim":
        try:
            if action == "Add":
                st.subheader("➕ Add New Claim")
                with st.form("add_claim"):
                    claim_id = st.number_input("Claim ID", min_value=1)
                    food_id = st.number_input("Food ID", min_value=1)
                    receiver_id = st.number_input("Receiver ID", min_value=1)
                    claim_date = st.date_input("Claim Date")
                    submitted = st.form_submit_button("Add Claim")
                if submitted:
                    add_claim(claim_id, food_id, receiver_id, claim_date.strftime('%Y-%m-%d'))
                    st.success("Claim added successfully!")

            elif action == "Update":
                st.subheader("✏️ Update Claim Date")
                claim_id = st.number_input("Claim ID to Update", min_value=1)
                new_date = st.date_input("New Claim Date")
                if st.button("Update Claim"):
                    update_claim_date(claim_id, new_date.strftime('%Y-%m-%d'))
                    st.success(f"Claim ID {claim_id} updated.")

            elif action == "Delete":
                st.subheader("🗑️ Delete Claim")
                claim_id = st.number_input("Claim ID to Delete", min_value=1)
                if st.button("Delete Claim"):
                    delete_claim(claim_id)
                    st.warning(f"Claim ID {claim_id} deleted.")
        except Exception as e:
            st.error("An error occurred while performing the CRUD operation.")
            st.exception(e)


elif page == "SQL Queries & Visualization":
    st.title("📊 SQL Queries & Visualization")

    questions = {
        "1. How many food providers and receivers are there in each city?": "q1",
        "2. Which type of food provider contributes the most?": "q2",
        "3. Contact information of food providers in a specific city": "q3",
        "4. Which receivers have claimed the most food?": "q4",
        "5. Total quantity of food available from all providers": "q5",
        "6. City with the highest number of food listings": "q6",
        "7. Most commonly available food types": "q7",
        "8. How many food claims have been made for each food item?": "q8",
        "9. Which provider has had the highest number of successful claims?": "q9",
        "10. What percentage of food claims are completed vs. pending vs. canceled?": "q10",
        "11. What is the average quantity of food claimed per receiver?": "q11",
        "12. Which meal type is claimed the most?": "q12",
        "13. Total quantity of food donated by each provider": "q13",
        "14. Trend of food claims over time": "q14",
        "15. City with the highest food demand based on claims": "q15"
    }

    selected_question = st.selectbox("Choose a question to analyze", list(questions.keys()))
    qid = questions[selected_question]

    st.subheader(selected_question)

    try:
      
        if qid == "q1":
            provider_city = providers_df['City'].value_counts()
            receiver_city = receivers_df['City'].value_counts()
            merged = pd.concat([provider_city, receiver_city], axis=1, keys=['Providers', 'Receivers']).fillna(0)
            st.dataframe(merged.astype(int))

        elif qid == "q2":
            top_type = providers_df['Type'].value_counts().reset_index()
            top_type.columns = ['Provider Type', 'Count']
            st.dataframe(top_type)

        elif qid == "q3":
            city = st.text_input("Enter city name:")
            if city:
                filtered = providers_df[providers_df['City'].str.lower() == city.lower()]
                st.dataframe(filtered[['Name', 'Contact']])

        elif qid == "q4":
          top_receivers = claims_df.groupby('Receiver_ID').size().reset_index(name='Claim_Count')
          top_receivers = top_receivers.sort_values(by='Claim_Count', ascending=False)
          st.dataframe(top_receivers)

        elif qid == "q5":
         total_quantity = food_listings_df['Quantity'].sum()
         st.write(f"Total Quantity of Food: {total_quantity}")

        elif qid == "q6":
         merged_df = pd.merge(food_listings_df, providers_df[['Provider_ID', 'City']], on='Provider_ID', how='left')
         city_listing = merged_df['City'].value_counts().reset_index()
         city_listing.columns = ['City', 'Total Listings']
         st.dataframe(city_listing)

        elif qid == "q7":
          food_types = food_listings_df['Food_Type'].value_counts().reset_index()
          food_types.columns = ['Food Type', 'Count']
          st.dataframe(food_types)

        elif qid == "q8":
         food_claims = claims_df.groupby('Food_ID').size().reset_index(name='Claim_Count')
         food_claims = food_claims.sort_values(by='Claim_Count', ascending=False)
         st.dataframe(food_claims)

        elif qid == "q9":
         data = get_provider_with_most_claims()
         df = pd.DataFrame(data, columns=["Provider_Name", "Successful_Claims"])
         st.dataframe(df)

        elif qid == "q10":
         data = get_claim_status_distribution()
         df = pd.DataFrame(data, columns=["Claim_Status", "Count"])
         st.dataframe(df)

        elif qid == "q11":
         avg_quantity_per_receiver = claims_df.groupby('Receiver_ID')['Quantity'].mean().reset_index()
         avg_quantity_per_receiver.columns = ['Receiver ID', 'Avg Quantity Claimed']
         st.dataframe(avg_quantity_per_receiver)

        elif qid == "q12":
         most_claimed_meal = food_listings_df['Meal_Type'].value_counts().reset_index()
         most_claimed_meal.columns = ['Meal Type', 'Count']
         st.dataframe(most_claimed_meal)

        elif qid == "q13":
         food_by_provider = food_listings_df.groupby('Provider_ID')['Quantity'].sum().reset_index()
         food_by_provider.columns = ['Provider ID', 'Total Quantity Donated']
         st.dataframe(food_by_provider)

        elif qid == "q14":
         # Example if actual column is 'Date_Claimed'
          data = get_food_claims_trend()
          df = pd.DataFrame(data, columns=['Claim_Date', 'Total_Claims'])
          df['Claim_Date'] = pd.to_datetime(df['Claim_Date'])  # Optional, for formatting
          st.line_chart(df.set_index('Claim_Date'))

        elif qid == "q15":
         merged_claims = pd.merge(claims_df, receivers_df[['Receiver_ID', 'City']], on='Receiver_ID', how='left')
         city_demand = merged_claims['City'].value_counts().reset_index()
         city_demand.columns = ['City', 'Claim Count']
         st.dataframe(city_demand)


    except Exception as e:
        st.error("An error occurred while processing the SQL query.")
        st.exception(e)


elif page == "Learner SQL Queries":
    st.title("🎓 Learner SQL Queries")
    st.write("Explore learner-level SQL queries below.")

    questions = {
        "Total Number of Providers": get_total_providers,
        "Total Number of Receivers": get_total_receivers,
        "Total Number of Food Listings": get_total_food_listings,
        "Total Number of Claims": get_total_claims,
        "Total Quantity of Food Provided": get_total_quantity_provided,
        "Types of Food Available": get_food_types_available,
        "Providers by Location": get_providers_by_location,
        "Receivers by Location": get_receivers_by_location,
        "Food Listings by Provider": get_food_listings_by_provider,
        "Most Claimed Food Type": get_most_claimed_food_type
    }

    selected_question = st.selectbox("Choose a question to analyze", list(questions.keys()))
    qid = questions[selected_question]

    st.subheader(selected_question)

    if st.button("Run Query"):
        result = qid()
        st.dataframe(result)
        
elif page == "User Introduction":
    st.title("👤 User Introduction")
    st.info("""
        Hello! I'm Vinothkumar, a Data Science enthusiast currently working on a project titled 
        'Local Food Wastage Management System.' I am passionate about using data analysis 
        and technology to tackle important issues like food wastage and social good.
        
        ## About the Project:
        The 'Local Food Wastage Management System' aims to reduce food wastage by efficiently managing 
        food donations between local providers and receivers. The system helps in tracking food items, 
        managing claims, and visualizing trends in food donations, making it easier for users to interact 
        and contribute to reducing food waste.

        I am always excited to learn and improve my skills in data science and technology, and I'm eager 
        to contribute to meaningful and impactful projects.
    """)
 
        
        

