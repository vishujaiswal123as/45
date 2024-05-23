import pymysql
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load the database connection details from secrets.toml
load_dotenv()
db_config = {
    "host": st.secrets["mysql"]["host"],
    "user": st.secrets["mysql"]["user"],
    "password": st.secrets["mysql"]["password"],
    "database": st.secrets["mysql"]["database"],
}

# Connect to the MySQL database
connection = pymysql.connect(**db_config)

# Create a function to insert a new row into the table


def insert_row(name, pet):
    columns = ["name", "pet"]
    values = (name, pet)
    insert_query = "INSERT INTO mytable (name, pet) VALUES (%s, %s)"
    with connection.cursor() as cursor:
        cursor.execute(insert_query, values)
        connection.commit()

# Create a function to update a row in the table


def update_row(old_name, new_name, new_pet):
    update_query = f"UPDATE mytable SET name='{new_name}', pet='{new_pet}' WHERE name='{old_name}'"
    with connection.cursor() as cursor:
        cursor.execute(update_query)
        connection.commit()

# Create a function to delete a row from the table


def delete_row(name):
    delete_query = f"DELETE FROM mytable WHERE name='{name}'"
    with connection.cursor() as cursor:
        cursor.execute(delete_query)
        connection.commit()

# Create a function to read rows from the table based on name and pet


def read_rows(name, pet):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM mytable WHERE name=%s AND pet=%s", (name, pet))
        result = cursor.fetchall()
        if result:
            return result
        else:
            return None


# Set up the SQL query

def table():
    query = "SELECT * FROM mytable"
# Execute the query and retrieve the data
    data = pd.read_sql(query, connection)
    # Display the data
    st.dataframe(data)


def main1():

    with st.expander("CRUD"):
        # select=st.selectbox('Select',['Insert','Update','Delete'])
        # if select=="Insert":
        st.title("CRUD Operations With MySQL")
        # Display Options for CRUD Operations
        option = st.selectbox(
            "Select an Operation", ("Create", "Read", "Update", "Delete", 'Table'))
        return option
        # Perform Selected CRUD Operations


def main(option):
    if option == "Create":
        st.subheader("Create a Record")
        name = st.text_input("Enter Name")
        pet = st.text_input("Enter pet")
        if st.button("Create"):
            insert_row(name, pet)
            st.write("Record created successfully.")

    elif option == "Read":
        st.subheader("Read Records")
        name = st.text_input("Enter Name")
        pet = st.text_input("Enter pet")
        specific_data = read_rows(name, pet)
        # Use the read_rows function to fetch specific rows
    #   specific_data = read_rows("some_name", "some_pet")
        if specific_data is not None:
            for data in specific_data:
                st.write("Name:", data[0])
                st.write("Pet:", data[1])
        else:
            st.write("No data found for the given name and pet.")

    elif option == "Update":
        st.subheader("Update a Record")
    #   id=st.number_input("Enter ID",min_value=1)
        name = st.text_input("Enter old Name")
    #   pet = st.text_input("Enter old pet")
        new_name = st.text_input("Enter New Name")
        new_pet = st.text_input("Enter New pet")
        if st.button("Update"):
            update_row(name, new_name, new_pet)
            st.write("Record updated successfully.")
            
    elif option == "Delete":
        st.subheader("Delete a Record")
    #   id=st.number_input("Enter ID",min_value=1)
        name = st.text_input("Enter old Name")
    #   pet = st.text_input("Enter old pet")
        if st.button("Delete"):
            delete_row(name)
            st.write("Record deleted successfully.")

    elif option == 'Table':
        table()


if __name__ == "__main__":
    #  connection_info()
    main(main1())
