import streamlit as st
import mysql.connector

# now automate

def connection_info():
   with st.expander('Connect Mysql server'):
    user = st.text_input('User', help='Optional Default it root')
    password = st.text_input('Password', type='password')
    dbms = st.text_input(
        'Database name', help='Make sure you have created database pets and mytable inside it')
    return password, dbms, user


def create_connection(password, dbms, user='root'):
    if password and dbms:
        connection = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database=dbms
        )
        return connection

passw,dbms,user=connection_info()
if dbms and passw: 
  connection = create_connection(passw,dbms,user)

# # vishu123930@@
def create_record(name, pet):
    #  connection = create_connection()
    cursor = connection.cursor()

    query = "INSERT INTO mytable VALUES (%s, %s)"
    value = (name, pet)

    cursor.execute(query, value)
    connection.commit()
    st.write(f"{cursor.rowcount} record inserted.")


def read_records():
    #  connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM mytable"

    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        st.write(row)


def update_record(name, pet, new_name, new_pet):
    #  connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE mytable SET name=%s, pet=%s WHERE name=%s AND pet=%s"
    value = (new_name, new_pet, name, pet)

    cursor.execute(query, value)
    connection.commit()

    st.write(f"{cursor.rowcount} record updated.")


def delete_record(name, pet):
    #  connection = create_connection()
    cursor = connection.cursor()

    query = "DELETE FROM mytable WHERE name=%s AND pet=%s"
    value = (name, pet)

    cursor.execute(query, value)
    connection.commit()

    st.write(f"{cursor.rowcount} record deleted.")

# # Create Streamlit App


def main():
    st.title("CRUD Operations With MySQL")

    # Display Options for CRUD Operations
    option = st.sidebar.selectbox(
        "Select an Operation", ("Create", "Read", "Update", "Delete"))
    # Perform Selected CRUD Operations
    if option == "Create":
        st.subheader("Create a Record")
        name = st.text_input("Enter Name")
        pet = st.text_input("Enter pet")
        if st.button("Create"):
            create_record(name, pet)

    elif option == "Read":
        st.subheader("Read Records")
        read_records()

    elif option == "Update":
        st.subheader("Update a Record")
      #   id=st.number_input("Enter ID",min_value=1)
        name = st.text_input("Enter old Name")
        pet = st.text_input("Enter old pet")
        new_name = st.text_input("Enter New Name")
        new_pet = st.text_input("Enter New pet")
        if st.button("Update"):
            update_record(name, pet, new_name, new_pet)

    elif option == "Delete":
        st.subheader("Delete a Record")
      #   id=st.number_input("Enter ID",min_value=1)
        name = st.text_input("Enter old Name")
        pet = st.text_input("Enter old pet")
        if st.button("Delete"):
            delete_record(name, pet)


if __name__ == "__main__":
    #  connection_info()
    main()
