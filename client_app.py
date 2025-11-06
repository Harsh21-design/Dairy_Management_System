import asyncio
import json
import pandas as pd
import streamlit as st
import datetime
from streamlit_option_menu import option_menu
from fastmcp import Client
from fastmcp.client import StreamableHttpTransport

# Add client
transport = StreamableHttpTransport("http://localhost:8000/mcp")
client = Client(transport=transport)

# Client - Server Connection Test
async def connection():
    async with client:
        # Basic server interaction
        await client.ping()
        print("CONNECTED TO MCP SERVER!!")

# asyncio.run(connection())

# FIRST TOOL - Add customer
async def add_customer(name,phone,date):
    async with client:
        resp_1 = await client.call_tool(
            "add_customer",
            {
                "name":name,
                "phone":phone,
                "date":date
            }
        )
        return resp_1.content[0].text

# SECOND TOOL - Add milk entry
async def add_milk_entry(customer_id,quantity_in_litres,additional_qty,amount,day,month,year):
    async with client:
        resp_2 = await client.call_tool(
            "add_milk_entry",
            {
                "customer_id":customer_id,
                "quantity_in_litres":quantity_in_litres,
                "additional_qty":additional_qty,
                "amount":amount,
                "day":day,
                "month":month,
                "year":year
                # "date":date
            }
        )
    return resp_2.content[0].text

# THIRD TOOL - Total Monthly Bill for a single customer
async def monthly_bill(customer_id, month, year):
    async with client:
        resp_3 = await client.call_tool(
            "monthly_bill",
            {
                "customer_id":customer_id,
                "month":month,
                "year":year
            }

        )
    return resp_3.content[0].text
    

# FOURTH TOOL - Customer List
async def customer_list():
    async with client:
        resp_4 = await client.call_tool(
            "customer_list",
            {}
        )
    return resp_4.content[0].text

# FIFTH TOOL - Milk Entries for single customer
async def milk_entries(customer_id):
    async with client:
        resp_5 = await client.call_tool(
            "milk_entries",
            {
                "customer_id":customer_id
            }
        )
    return resp_5.content[0].text

# STREAMLIT UI
# st app configuration
st.set_page_config(page_title="Dairy Management",
                   page_icon="milk-bottle",
                   layout="wide")


# sidebar navigation
with st.sidebar:
    page = option_menu(
        menu_title="🥛My Dairy App",
        menu_icon="🥛",
        options=["🏠 Home","👤 Add Customer","➕ Add Milk Entry","🧾 Get Monthly Bill","📋 Get Customer List","🗒️ Get Milk Entry List"]
    )

if page == "🏠 Home":
    st.title("🥛DAIRY MANAGEMENT SYSTEM🥛")
    st.header("Welcome to My Dairy App!")
    st.subheader("A Dairy Management System using MCP, SQLiteDB and Streamlit")
    st.markdown("##### Manage all your Dairy related operations with My Dairy App using Sidebar Navigation.")
    # st.markdown("Different operations of My Dairy App are listed below:")
    # st.write("1. Adding New Customers \n2. Adding & Viewing Milk Entries \n3. Getting Total Monthly Bills \n4. Viewing Customer List")

elif page == "📋 Get Customer List":
    st.header("My Dairy Customers")
    st.markdown("### List down all customers of My Dairy App.")
    if st.button("Show All"):
        try:
            with st.spinner("showing..."):
                get = asyncio.run(customer_list())
                # st.success(get)
                data = json.loads(get)
                # customers = data["customers"]
                df = pd.DataFrame(data,
                                  columns=["ID","Name","Phone","Date"])
                st.dataframe(df)
        except IndexError:
            st.warning("No customers found in the database!")

elif page == "👤 Add Customer":
    st.header("Add A New Customer")
    st.markdown("#### Fill below details to add a new customer in My Dairy App.")
    name = st.text_input("Enter Customer Name:-")
    phone = st.text_input("Enter Customer Phone Number:-")
    date = st.date_input("Enter Customer Registration Date:-",value=datetime.date.today())
    if st.button("Add New"):
        if  name and phone and date:
            with st.spinner("Adding..."):
                get = asyncio.run(add_customer(name,phone,date))
                st.markdown(f"## **Customer Added Successfully at customer ID number: {get}**")
        else:
            st.warning("Please enter all the details to add a new customer!")

elif page == "➕ Add Milk Entry":
    st.header("Add A New Milk Entry")
    st.markdown("#### Fill below details to add a new milk entry for a particular customer ID.")
    customer_id = st.text_input("Enter Customer ID :-")
    quantity_in_litres = st.number_input("Enter Milk Quantity In Litres :-",value=0)
    additional_qty = st.number_input("Enter Additional Quantity :-",value=0)
    amount = st.number_input("Enter Total Amount :-")
    day = st.selectbox("Select Day :-", options=list(range(1, 32)))
    month = st.selectbox("Select Month :-", options=list(range(1, 13)))
    year = st.selectbox("Select Year :-", options=list(range(2020, 2051)))
    # date = st.date_input("Enter Date:-",value=datetime.date.today())
    if st.button("Add New Entry"):
        if customer_id and quantity_in_litres and amount and day and month and year or additional_qty:
        # if customer_id and quantity_in_litres and amount and date:
            with st.spinner("Adding..."):
                # get = asyncio.run(add_milk_entry(customer_id,quantity_in_litres,additional_qty,amount,day,month,year))
                get = asyncio.run(add_milk_entry(customer_id,quantity_in_litres,additional_qty,amount,day,month,year))
                st.markdown(f"## **New Milk Entry Added Successfully for Customer ID: {customer_id}**")
        else:
            st.warning("Please enter all the details to add a new milk entry!")
    
elif page == "🗒️ Get Milk Entry List":
    st.header("Get Milk Entries for a Particular Customer ID ")
    st.markdown("#### Fill Below details to get the total milk entries.")
    customer_id = st.text_input("Enter Customer ID :-")
    if st.button("Show all entries"):
        if customer_id:
            with st.spinner("Showing..."):
                get = asyncio.run(milk_entries(customer_id))
                # st.success(f"Total Milk Entries for Customer ID {customer_id} : \n{get}")
                data_entry = json.loads(get)
                df = pd.DataFrame(data_entry,
                                  columns=["Sr No","Customer ID","Quantity(Litres)","Additional Quantity","Amount","Day","Month","Year"])
                st.dataframe(df)
        else:
            st.warning("Please enter a valid Customer ID")

elif page == "🧾 Get Monthly Bill":
    st.header("Get Monthly Bill for a Particular Customer ID ")
    st.markdown("#### Fill Below details to get the total monthly bill.")
    customer_id = st.text_input("Enter Customer ID :-")
    month = st.selectbox("Select Month :-", options=list(range(1, 13)))
    year = st.selectbox("Select Year :-", options=list(range(2020, 2051)))
    if st.button("Show Bill"):
        if customer_id and month and year:
            with st.spinner("Showing..."):
                get = asyncio.run(monthly_bill(customer_id,month,year))
                st.markdown(f"## **Total Monthly Bill for Customer ID {customer_id}:**")
                st.markdown(f"## Rs.{get}")
        else:
            st.warning("Please enter all the details to get the monthly bill!")