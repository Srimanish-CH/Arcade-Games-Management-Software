import streamlit as st
import mysql.connector
import pandas as pd
from PIL import Image
from datetime import date
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


min_value=date.today()
max_value= date.today() + timedelta(days=365)


# CREATING PROCEDURE:


# Get the current date
current_date = date.today()
# Calculate the expiry date for the same day next year
next_year_date = current_date.replace(year=current_date.year + 1)



# Main content

arrow = "➡️"
coin = "🪙"
joystick = "🎮"
ticket = "🎟️"
credit_card = "💳"
money = "💸"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="ARCADE_GAMES_MANAGEMENT_SYSTEM"
)


# Placeholder for staff login logic (replace with your actual logic)
def check_staff_login(username, password):
    # Connect to your staff database and perform the login check
    # Replace the following lines with your actual logic

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM staff WHERE staff_username = %s AND staff_password = %s", (username, password))
    staff = cursor.fetchone()
    cursor.close()
    

    return staff
def get_game_categories_and_games():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gamecategories")
    game_categories = cursor.fetchall()

    game_data = {}
    for category in game_categories:
        cursor.execute("SELECT * FROM games WHERE GameCategory = %s", (category['CategoryID'],))
        games = cursor.fetchall()
        game_data[category['Genre']] = games

    cursor.close()
    
    return game_data

# Function to retrieve customer data
def get_customer_data(username, password):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Customers WHERE Username = %s AND Password = %s", (username, password))
    customer = cursor.fetchone()
    cursor.close()
    
    return customer
def update_machine_status(machine_id, new_status):
    cursor = db.cursor()
    cursor.execute("UPDATE machines SET Status = %s WHERE MachineID = %s", (new_status, machine_id))
    #db.commit()
    cursor.close()

# Function to update customer's membership count
def update_membership_count(customer_id, new_count):
    cursor = db.cursor()
    cursor.execute("UPDATE Customers SET MembershipsCount = %s WHERE CustomerID = %s", (new_count, customer_id))
    db.commit()
    cursor.close()

# Function to view CustomerTokenLog
def view_customer_token_log():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM CustomerTokenLog")
    token_log = cursor.fetchall()
    cursor.close()

    # Display CustomerTokenLog in a DataFrame
    token_log_df = pd.DataFrame(token_log, columns=["LogID", "CustomerID", "OldTokens", "NewTokens", "Timestamp"])
    st.dataframe(token_log_df)


# Call the create_trigger function to create the trigger




# Initialize session state
st.session_state.customer_data = st.session_state.get('customer_data', None)
st.session_state.staff_data = st.session_state.get('staff_data', None)

st.sidebar.title("MENU")
selected_tab = st.sidebar.radio("", ("WELCOME PAGE","CUSTOMER PAGE", "STAFF PAGE"))

# Customer functionality
if selected_tab == "WELCOME PAGE":
    # Display welcome message and image
    #image_path = r'C:\Users\srima\Desktop\AGMS\arcade.jpg'
    #image_path = 'C:/Users/srima/Desktop/AGMS/arcade.jpg'
    #image = Image.open(image_path)
    st.title(f" {joystick} WELCOME TO FUN WORLD !!!")
    #st.image(image, caption='', use_column_width=True)
    st.write("---------------------------------------------------")
    st.subheader("GAMES CATALOGUE : ")

# Retrieve game categories and games
    game_data = get_game_categories_and_games()
        # Display game categories and games
    i = 1
    for category, games in game_data.items():
            st.write(f"*{category}* : ")
            for game in games:
                st.write(i, f" {game['Name']} ")
                i = i + 1

    st.write("---")

def update_machine_status(machine_id, new_status):
    cursor = db.cursor()
    
    # Get the old status before the update
    cursor.execute("SELECT Status FROM machines WHERE MachineID = %s", (machine_id,))

    old_status = cursor.fetchone()[0]
    
    # Update the machine status
    cursor.execute("UPDATE machines SET Status = %s WHERE MachineID = %s", (new_status, machine_id))
    db.commit()
    
    # Fetch the updated machine data
    cursor.execute("SELECT * FROM machines WHERE MachineID = %s", (machine_id,))
    new_machine_data = cursor.fetchone()
    
    # Add trigger to log status changes only if status has changed
    #if old_status != new_status:
        #cursor.execute("INSERT INTO MachineStatusLog (MachineID, OldStatus, NewStatus) VALUES (%s, %s, %s)",
                       #(machine_id, old_status, new_status))
    
    #db.commit()
    #cursor.close()



if selected_tab == "CUSTOMER PAGE":
    customer_option = st.sidebar.selectbox("CUSTOMER PAGES", ["LOGIN","PLAY GAMES","GIFT STORE","PURCHASE MEMBERSHIPS"])

    if customer_option == "LOGIN":
        st.subheader(f" {arrow} CUSTOMER LOGIN")
        customer_username = st.text_input("USERNAME")
        customer_password = st.text_input("PASSWORD", type="password")

        if st.button("LOGIN"):
            # Check the username and password against a database of customers
            customer = get_customer_data(customer_username, customer_password)

            if customer:
                # Customer is logged in
                st.session_state.customer_data = customer  # Save customer information in session state
                st.success("LOGIN SUCCESSFUL!")
                # Display remaining credits
                st.write(f" {coin} CREDIT BALANCE : {customer[5]} ")
            else:
                st.error("INCORRECT CREDENTIALS, PLEASE TRY AGAIN.")

    elif customer_option == "PLAY GAMES":
        # Display available games
        st.header(f" {joystick} GAMES:")
        # Retrieve and display available games from the database
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Games")
        games = cursor.fetchall()
        cursor.close()

        # Check if the customer is logged in
        for game in games:
                st.write(f"{joystick}*TITLE:* {game[2]}")
                st.write(f"*CREDITS REQUIRED:* {game[3]}")
                st.write(f"*TOKENS YOU CAN WIN:* {game[4]}")
                play_button_clicked = st.button(f"PLAY {game[2]}")

                # Check if the play button is clicked
                if play_button_clicked:
                    # Check if the customer is logged in
                    if not st.session_state.customer_data:
                        st.error("LOGIN REQUIRED, PLEASE HEAD TO THE CUSTOMER SECTION AND LOG IN.")
                    else:
                        # Check if credits are sufficient using the stored customer information
                        if st.session_state.customer_data[5] >= game[3]:
                            st.success("ENJOY YOUR GAME!!")
                            # Update customer credits
                            new_credits = st.session_state.customer_data[5] - game[3]
                            new_tokens = st.session_state.customer_data[8] + game[4]
                            cursor = db.cursor()
                            cursor.execute("UPDATE Customers SET CreditsRemaining = %s, tokens_gained = %s WHERE CustomerID = %s",
                                   (new_credits, new_tokens, st.session_state.customer_data[0]))
                            db.commit()
                            cursor.close()
                            st.session_state.customer_data = (
                                st.session_state.customer_data[0],
                                st.session_state.customer_data[1],
                                st.session_state.customer_data[2],
                                st.session_state.customer_data[3],
                                st.session_state.customer_data[4],
                                new_credits,  # Update the credits
                                st.session_state.customer_data[6],
                                st.session_state.customer_data[7],
                                new_tokens,
                            )    
                            

                            

                            # Decrement membership count if applicable
                            if st.session_state.customer_data[4] > 0:
                                updated_membership_count = st.session_state.customer_data[4] - 1
                                update_membership_count(st.session_state.customer_data[0], updated_membership_count)
                                st.session_state.customer_data = (
                                    st.session_state.customer_data[0],
                                    st.session_state.customer_data[1],
                                    st.session_state.customer_data[2],
                                    st.session_state.customer_data[3],
                                    updated_membership_count,  # Update MembershipsCount
                                    new_credits,  # Update the credits
                                    st.session_state.customer_data[6],
                                    st.session_state.customer_data[7],
                                    new_tokens,
                                )
                        else:
                            st.error("INSUFFICIENT CREDIT BALANCE ")
                st.write("----")


    elif customer_option == "PURCHASE MEMBERSHIPS":
        if not st.session_state.customer_data:
                st.error("LOGIN REQUIRED, PLEASE HEAD TO THE CUSTOMER SECTION AND LOG IN")
        else:
            buy_membership_customerid = st.session_state.customer_data[0]
            # Display available memberships
            st.header(f"{money}MEMBERSHIP PLANS :")
            memberships = {
            "PLATINUM": {"CREDITS": 3000, "PRICE": 5000},
            "GOLD": {"CREDITS": 1500, "PRICE": 2500},
            "SILVER": {"CREDITS": 1000, "PRICE": 1500}
            }

            for membership_plan, details in memberships.items():
                st.write(f"MEMBERSHIP: {membership_plan}")
                st.write(f"CREDITS: {details['CREDITS']}")
                st.write(f"PRICE: {details['PRICE']}")
                expiry_date = date.today() + timedelta(days=365)
                st.write(f"EXPIRY DATE: {expiry_date}")

            # Button to purchase membership
                if st.button(f"BUY {membership_plan}"):
                    
                    # Update customer's credits in the database
                    new_credits = st.session_state.customer_data[5] + details['CREDITS']
                    new_mem_count = int(st.session_state.customer_data[4]) + 1
                    #print(new_mem_count)
                    cursor = db.cursor()
                    cursor.execute("UPDATE Customers SET CreditsRemaining = %s WHERE CustomerID = %s", (new_credits, st.session_state.customer_data[0]))
                    cursor.execute("UPDATE Memberships SET Expiry_Date = %s WHERE CustomerID = %s AND MembershipPlan = %s",(expiry_date,buy_membership_customerid, membership_plan))
                    cursor.execute("UPDATE Memberships SET MembershipPlan = %s WHERE CustomerID = %s",(membership_plan,buy_membership_customerid))
                    cursor.execute("UPDATE Customers SET MembershipsCount = %s WHERE CustomerID = %s",(new_mem_count,buy_membership_customerid))
                    db.commit()
                    cursor.close()
                    updated_membership_count = st.session_state.customer_data[4] + 1
                    update_membership_count(st.session_state.customer_data[0], updated_membership_count)

                    st.session_state.customer_data = (
                    st.session_state.customer_data[0],
                    st.session_state.customer_data[1],
                    st.session_state.customer_data[2],
                    st.session_state.customer_data[3],
                    updated_membership_count,  # Update MembershipsCount
                    new_credits,  # Update the credits
                    st.session_state.customer_data[6],
                    st.session_state.customer_data[7]
                    )
                
                    
                    st.success(f"PURCHASE SUCCESSFUL. YOU HAVE PURCHASED {membership_plan} MEMBERSHIP PLAN. YOUR CREDIT BALANCE IS: {new_credits}")
                
    # ...

    elif customer_option == "GIFT STORE":
        # Display redeemable items in the store
        st.header(f"🎁 GIFT STORE")
        
        # Retrieve and display redeemable items from the database
        cursor = db.cursor()
        cursor.execute("SELECT * FROM RedeemableStore")
        redeemable_items = cursor.fetchall()
        cursor.close()
        
        for item in redeemable_items:
            st.write(f"🎁 PRODUCT: {item[1]}")
            st.write(f"PRICE: {item[2]} TOKENS")
            st.write(f"AVAILABILITY: {item[3]}")
            
            
            # Check if tokens are enough to buy the item
            get_it_button_clicked = st.button(f"PURCHASE {item[1]}")
            st.write("--------------------------------------------------")
            #print(st.session_state.customer_data)
            if get_it_button_clicked:
                # Check if the customer is logged in
                if not st.session_state.customer_data:
                    st.error("LOGIN REQUIRED, HEAD TO THE CUSTOMER SECTION TO LOG IN.")
                else:
                    # Check if tokens are sufficient
                    if int(st.session_state.customer_data[8]) >= int(item[2]):
                        st.success("PURCHASE SUCCESSFUL!.")
                        # Update customer's tokens_gained
                        new_tokens_gained = st.session_state.customer_data[8] - item[2]
                        cursor = db.cursor()
                        cursor.execute("UPDATE Customers SET tokens_gained = %s WHERE CustomerID = %s",
                                    (new_tokens_gained, st.session_state.customer_data[0]))
                        db.commit()
                        cursor.close()
                        st.session_state.customer_data = (
                            st.session_state.customer_data[0],
                            st.session_state.customer_data[1],
                            st.session_state.customer_data[2],
                            st.session_state.customer_data[3],
                            st.session_state.customer_data[4],
                            st.session_state.customer_data[5],
                            st.session_state.customer_data[6],
                            st.session_state.customer_data[7],
                            new_tokens_gained,
                        )
                        new_availability = item[3] - 1
                        cursor = db.cursor()
                        cursor.execute("UPDATE RedeemableStore SET Availability = %s WHERE ProductID = %s",
                                    (new_availability, item[0]))
                        db.commit()
                        cursor.close()
                        
                        st.session_state.customer_data = (
                            st.session_state.customer_data[0],
                            st.session_state.customer_data[1],
                            st.session_state.customer_data[2],
                            st.session_state.customer_data[3],
                            st.session_state.customer_data[4],
                            st.session_state.customer_data[5],
                            st.session_state.customer_data[6],
                            st.session_state.customer_data[7],
                            new_tokens_gained)
                    else:
                        st.error("INSUFFICIENT TOKEN, PLAY MORE GAMES TO EARN TOKENS.")
        

# ...





# Staff functionality
if selected_tab == "STAFF PAGE":
    staff_page = st.sidebar.selectbox("STAFF PAGES", ["LOGIN", "CUSTOMER DETAILS",  "MEMBERSHIPS",  "GIFT STORE INVENTORY", "MACHINES" , "UPDATE MACHINE STATUS" , "MACHINE STATUS LOGS","OVERVIEW OPTIONS"])

    if staff_page == "LOGIN":
        st.subheader(f" {arrow}STAFF LOGIN")
        staff_username = st.text_input("USERNAME")
        staff_password = st.text_input("PASSWORD", type="password")

        if st.button("LOGIN"):
            # Check the username and password against a database of staff
            staff = check_staff_login(staff_username, staff_password)

            if staff:
                # Staff is logged in
                st.session_state.staff_data = staff  # Save staff information in session state
                st.success("LOGIN SUCCESSFUL! ")
            else:
                st.error("INCORRECT CREDENTIALS, PLEASE TRY AGAIN.")

    elif staff_page == "CUSTOMER DETAILS":
            if not st.session_state.staff_data:
                st.error("LOGIN REQUIRED.")
            else:
                st.subheader("CUSTOMER DETAILS")
                # Retrieve all customer data and display in DataFrame
                cursor = db.cursor()
                cursor.execute("SELECT * FROM Customers")
                customers = cursor.fetchall()
                cursor.close()

                # Display customer data in DataFrame
                df_customers = pd.DataFrame(customers, columns=["CustomerID", "CustomerName", "PhoneNumber", "EmailID", "MembershipsCount", "CreditsRemaining", "Username", "Password", "tokens_gained"])

                st.dataframe(df_customers)

                st.write("-----------------------------------------")
            
                st.subheader("ADD CUSTOMER")
                # Get input for new customer
                new_username = st.text_input("USERNAME")
                new_password = st.text_input("PASSWORD", type="password")
                new_customer_name = st.text_input("NAME")
                new_phone_number = st.text_input("PHONE NUMBER")
                new_email_id = st.text_input("EMAIL ID")
                new_memberships_count = st.number_input("MEMBERSHIPS PURCHASED",step=1)
                new_credits_remaining = st.number_input("CREDIT BALANCE",step=1)
                new_tokens_gained = st.number_input("TOKENS EARNED",step=1)
                if st.button("Add"):
                    # Add new customer to the database
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO Customers (CustomerName, PhoneNumber, EmailID, MembershipsCount, CreditsRemaining, Username, Password , tokens_gained) VALUES (%s, %s, %s, %s, %s, %s, %s , %s)",
                                (new_customer_name, new_phone_number, new_email_id, new_memberships_count, new_credits_remaining, new_username, new_password , new_tokens_gained))
                    db.commit()
                    cursor.close()
                    st.success("NEW CUSTOMER ADDED SUCCESSFULLY!")
                

                st.write("----------------------------------------------------------------------------------")
                st.subheader("DELETE CUSTOMER")
                
                del_cust = st.number_input("CUSTOMER ID",step=1)
                if st.button("DELETE CUSTOMER"):
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM memberships WHERE CustomerID = %s" ,(del_cust,))
                    delete_query = "DELETE FROM customers WHERE CustomerID = %s"
                    cursor.execute(delete_query, (del_cust,))
                    db.commit()
                    cursor.close()
                    st.success("CUSTOMER DELETED SUCCESSFULLY!")
                    #except mysql.connector.Error as err:
                    #st.error(f"Error: {err}")
                

    elif staff_page == "MEMBERSHIPS":
            if not st.session_state.staff_data:
                st.error("LOGIN REQUIRED")
            else:
                st.subheader("MEMBERSHIP LOG DETAILS")
                # Retrieve all customer data and display in DataFrame
                cursor = db.cursor()
                cursor.execute("SELECT c.CustomerID, c.CustomerName, m.CardNumber, m.MembershipID, m.MembershipPlan, m.StartDate, m.Expiry_Date, c.CreditsRemaining FROM customers c JOIN memberships m ON c.CustomerID = m.CustomerID")
                memberships = cursor.fetchall()
                df_memberships = pd.DataFrame(memberships, columns=["Customer ID", "Customer Name", "Card Number", "Membership ID","Membership PLan", "StartDate", "EXPIRY_DATE" , "Credits Remaining"]).fillna('')
                st.dataframe(df_memberships)
                cursor.execute("SELECT SUM(MembershipsCount) AS TotalMemberships FROM customers;")
                mem_count = cursor.fetchall()
                df_mem_count = pd.DataFrame(mem_count, columns=["TOTAL NUMBER OF MEMBERSHIPS PURCHASED"])
                st.dataframe(df_mem_count)
                cursor.close()

                st.write("-----------------------------")
                # Add Memberships functionality
                st.subheader("ADD NEW MEMBERSHIP")
                expiry_date_2 = date.today() + timedelta(days=365)
                # Get input for new membership
                membership_plan = st.selectbox("MEMBERSHIP PLAN", ["PLATINUM", "GOLD","SILVER"])
                card_number = st.text_input("MEMBERSHIP CARD NUMBER")
                mem_customerid = st.number_input("CUSTOMER ID",step=1)
                start_date = st.date_input("START DATE", min_value=date.today())
                expiry_date_value = st.date_input("EXPIRY DATE", min_value = expiry_date_2 ,value = expiry_date_2)
                #price = st.number_input("Price")
                default_price = 0  # Default to 0 if membership plan is not recognized
                default_credits = 0
                
                if membership_plan == "SILVER":
                    default_price = 1500
                elif membership_plan == "GOLD":
                    default_price = 2500
                elif membership_plan == "PLATINUM":
                    default_price = 5000

                price = st.number_input("PRICE", value=default_price)

                
                if membership_plan == "SILVER":
                    default_credits = 1000
                elif membership_plan == "GOLD":
                    default_credits = 1500
                elif membership_plan == "PLATINUM":
                    default_credits = 3000

                credits = st.number_input("CREDITS", value=default_credits)


                if st.button("ADD MEMBERSHIP"):
                    update_mem_count= 1
                    # Add new membership to the database
                    cursor = db.cursor()
                    # Assuming that 'mem_customerid' is the CustomerID of the customer making the purchase
                    cursor.execute("INSERT INTO Memberships (MembershipPlan, CardNumber, CustomerID, Credits, StartDate, EXPIRY_DATE, Price) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (membership_plan, card_number, mem_customerid, credits, start_date, expiry_date_2, price))
                    
                    cursor.execute("UPDATE Customers SET MembershipsCount = MembershipsCount + %s , CreditsRemaining = CreditsRemaining + %s WHERE CustomerID = %s",
                                (update_mem_count,credits, mem_customerid))
                    db.commit()
                    cursor.close()
                    st.success("MEMBERSHIP ADDED SUCCESSFULLY")
                    
        
        

    elif staff_page == "GIFT STORE INVENTORY":
        if not st.session_state.staff_data:
            st.error("LOGIN REQUIRED")
        else:
            st.subheader("GIFT STORE INVENTORY")

            # Retrieve redeemable items from the database
            cursor = db.cursor()
            cursor.execute("SELECT * FROM RedeemableStore")
            redeemable_items = cursor.fetchall()
            cursor.close()

            # Display redeemable items in DataFrame
            df_redeemable_store = pd.DataFrame(redeemable_items, columns=["ProductID", "ProductName", "tokens_required", "Availability"])
            st.dataframe(df_redeemable_store)

            st.subheader("ADD NEW PRODUCT")
                # Get input for new customer
            new_productname = st.text_input("PRODUCT NAME")
            new_product_Tokens = st.number_input("TOKENS REQUIRED", step = 1)
            new_product_availability = st.number_input("AVAILABILITY",step = 1)
            
            if st.button("ADD NEW PRODUCT"):
                # Add new customer to the database
                cursor = db.cursor()
                
                cursor.execute("INSERT INTO redeemablestore (ProductName, tokens_required, Availability) VALUES (%s, %s, %s)",
                                (new_productname, new_product_Tokens, new_product_availability))
                db.commit()
                cursor.close()
                st.success("PRODUCT ADDED SUCCESSFULLY!!")


            # UPDATE PRODUCT AVAILABILITY
            st.subheader("UPDATE PRODUCT AVAILABILITY")
            update_product_productid = st.number_input("PRODUCT ID", step = 1)

            # Creating a new key for Updated availability to avoid duplicate key issue 
            
            upd_availability = "unique_key_for_availability_input"
            update_product_availability = st.number_input("AVAILABILITY",step = 1, key = upd_availability)
            print(st.session_state.customer_data)
            if st.button("UPDATE PRODUCT AVAILABILITY"):
                cursor = db.cursor()
                cursor.execute("UPDATE redeemablestore SET Availability = %s WHERE ProductID = %s",
                (update_product_availability,  update_product_productid))
                

                db.commit()
                cursor.close()
                st.success("PRODUCT AVAILABILITY UPDATED!!")



    elif staff_page == "MACHINES":
        if not st.session_state.staff_data:
            st.error("LOGIN REQUIRED")
        else:
            st.subheader("ARCADE MACHINES DETAILS")
            # Retrieve all machine data and display in DataFrame
            cursor = db.cursor()
            cursor.execute("SELECT * FROM machines")
            machines = cursor.fetchall()
            cursor.close()

            # Display machine data in DataFrame
            machine_df = pd.DataFrame(machines, columns=["MachineID", "GameID", "GameCategory", "Status"])

            # Display machines in DataFrame with custom formatting
            st.dataframe(machine_df.style.apply(lambda x: ['background: lightgreen' if x['Status'] == 'Working' else 'background: red' for _ in x], axis=1))

        st.write("----------------------------------------------------------------------")
        
        st.subheader("ADD NEW MACHINE")
                # Get input for new machine
        new_game_id = st.number_input("Game ID", step=1)
        new_game_category = st.number_input("Game Category", step=1)
        new_status = st.selectbox("Status", ["Running", "Stand_by"])

        if st.button("ADD NEW MACHINE"):
                # Add new machine to the database
            cursor = db.cursor()
            cursor.execute("INSERT INTO machines (GameID, GameCategory, Status) VALUES (%s, %s, %s)",
                                        (new_game_id, new_game_category, new_status))
            db.commit()
            cursor.close()
            st.success("NEW MACHINE ADDED SUCCESSFULLY!")

    elif staff_page == "UPDATE MACHINE STATUS":
        if not st.session_state.staff_data:
            st.error("LOGIN REQUIRED")
        else:
            st.subheader("CHANGE MACHINE STATUS")
        
            # Input for changing status to 'Working'
            machine_id_working = st.number_input("ENTER MACHINE ID TO SET STATUS AS 'RUNNING'", step =1)
            change_working_button = st.button("SET STATUS TO RUNNING'")
                
            if change_working_button:
                update_machine_status(machine_id_working, 'RUNNING')
                st.success(f"MACHINE {machine_id_working} STATUS UPDATED TO 'RUNNING'.")

                # Input for changing status to 'Not_working'
            machine_id_not_working = st.number_input("ENTER MACHINE ID TO SET STATUS AS 'STAND_BY'",step=1)
            change_not_working_button = st.button(" SET STATUS TO 'STAND_BY'")
                
            if change_not_working_button:
                update_machine_status(machine_id_not_working, 'STAND_BY')
                st.success(f"MACHINE {machine_id_not_working} STATUS UPDATED TO 'STAND_BY'.")

    elif staff_page == "MACHINE STATUS LOGS":
        st.subheader("MACHINE STATUS LOGS")

        # Retrieve and display MachineStatusLog table
        cursor = db.cursor()
        cursor.execute("SELECT * FROM MachineStatusLog")
        machine_status_log = cursor.fetchall()
        cursor.close()
        log_df = pd.DataFrame(machine_status_log, columns=["LogID", "MachineID", "OldStatus", "NewStatus", "Timestamp"])
        st.dataframe(log_df)

        st.write("--------------------------------------------------------")

        # Add a button to view CustomerTokenLog
        #st.subheader("Token Change Log")
        # Call the function to view CustomerTokenLog
        #view_customer_token_log()

    elif staff_page == "Change machine status":
        if not st.session_state.staff_data:
            st.error("Login required. Please go back to the staff section and log in.")
        else:
            st.subheader("Change Machine Status")
        
            # Input for changing status to 'Working'
            machine_id_working = st.number_input("Enter Machine ID to change status to 'Running'")
            change_working_button = st.button("Change Status to 'Stand_by'")
                
            if change_working_button:
                update_machine_status(machine_id_working, 'Running')
                st.success(f"Machine {machine_id_working} status updated to 'Stand_by'.")

                # Input for changing status to 'Not_working'
            machine_id_not_working = st.number_input("Enter Machine ID to change status to 'Running'")
            change_not_working_button = st.button("Change Status to 'Stand_by'")
                
            if change_not_working_button:
                update_machine_status(machine_id_not_working, 'Running')
                st.success(f"Machine {machine_id_not_working} status updated to 'Stand_by'.")


    elif staff_page == "OVERVIEW OPTIONS":
        if not st.session_state.staff_data:
            st.error("LOGIN REQUIRED.")

        else:
            st.subheader("SYSTEM OVERIVIEW FOR MAINTAINANCE")

            if st.button("VIEW GAMES UNDER SPORTS AND RACING CATEGORY"):
                # Retrieve and display MachineStatusLog table
                
                st.write("GAMES UNDER SPORTS CATEGORY")
                cursor = db.cursor()
                cursor.execute("SELECT g.GameID, g.Name AS GameName, COUNT(DISTINCT m.MachineID) AS MachineCount FROM games g LEFT JOIN machines m ON g.GameID = m.GameID WHERE g.GameCategory = (SELECT CategoryID FROM gamecategories WHERE Genre = 'Sports') GROUP BY g.GameID, g.Name")
                sport_games = cursor.fetchall()
                cursor.close()

                
                cursor = db.cursor()
                cursor.execute("SELECT g.GameID, g.Name AS GameName, COUNT(DISTINCT m.MachineID) AS MachineCount FROM games g LEFT JOIN machines m ON g.GameID = m.GameID WHERE g.GameCategory = (SELECT CategoryID FROM gamecategories WHERE Genre = 'Racing') GROUP BY g.GameID, g.Name")
                racing_games = cursor.fetchall()
                cursor.close()

                # Display MachineStatusLog in a DataFrame
                sport_games_df = pd.DataFrame(sport_games, columns=["GameID","GameName","No. of Machines"])
                st.dataframe(sport_games_df)

                st.write("GAMES UNDER RACING CATEGORY")
                  # Display MachineStatusLog in a DataFrame
                racing_games_df = pd.DataFrame(racing_games, columns=["GameID","GameName","No. of Machines"])
                st.dataframe(racing_games_df)


                st.write("--------------------------------------------------------")

            if st.button("VIEW MACHINES COUNT FOR EACH CATEGORY"):
                # Retrieve and display MachineStatusLog table
                st.write("MACHINES COUNT IN GAME CATEGORIES")
                cursor = db.cursor()
                cursor.execute("SELECT gc.Genre, COUNT(m.MachineID) AS TotalMachines FROM gamecategories gc LEFT JOIN machines m ON gc.CategoryID = m.GameCategory GROUP BY gc.Genre")
                machines_cat = cursor.fetchall()
                cursor.close()

                
                # Display MachineStatusLog in a DataFrame
                machines_cat_df = pd.DataFrame(machines_cat, columns=["Game Category","Machine Count"])
                st.dataframe(machines_cat_df)

                st.write("--------------------------------------------------------")


            if st.button("VIEW MACHINE ON STAND BY"):
            
                cursor = db.cursor()
                cursor.callproc("GetMachineGames", [])
                # Fetch the results
                results = cursor.stored_results()
                rows = []
                for result in results:
                    rows.extend(result.fetchall())
                    
                    
                if rows:
                    columns = ["MACHINE ID", "STATUS", "GAME ID", "GAME NAME", "CREDITS REQUIRED"]
                    st.table(pd.DataFrame(rows, columns=columns))
                
                else:
                    st.write("ALL MACHINES ARE RUNNING. GREAT WORK!!")

            # Close the cursor and database connection
                cursor.close()
                st.write("--------------------------------------------------------")
                    
                
                # Execute the procedure
                #cursor.execute(procedure_call, multi=True)
                # Fetch the results
                #results = cursor.fetchall()
                #print("Results:", results)
                # Display the results in Streamlit
                #for result in results:
                    #st.write(f"Machine ID: {result[0]}, Game ID: {result[2]}, Game Name: {result[3]}, Credits Required: {result[4]}, Status: {result[1]}")

                # Close the cursor and database connection
            #cursor.close()
            
            #st.write("--------------------------------------------------------")

                