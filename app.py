import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB Connection
client = MongoClient(
    "mongodb+srv://devkumar:dev89866@cluster0.kgk4tx3.mongodb.net/?appName=Cluster0"
)

db = client["student_db"]
collection = db["students"]

st.set_page_config(page_title="Student Management System")

st.title("🎓 Student Management System")

menu = st.sidebar.selectbox(
    "Select Option",
    ["Add Student", "View Students", "Search Student", "Delete Student"]
)

# Add Student
if menu == "Add Student":

    st.subheader("Add New Student")

    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")
    course = st.selectbox(
        "Course",
        ["BCA", "BBA", "MCA", "MBA", "B.Tech"]
    )
    age = st.number_input("Age", 1, 100)

    if st.button("Save"):

        if name and roll:

            data = {
                "name": name,
                "roll": roll,
                "course": course,
                "age": age
            }

            collection.insert_one(data)

            st.success("Student Added Successfully!")

        else:
            st.error("Fill all fields")

# View Students
elif menu == "View Students":

    st.subheader("Student Records")

    data = list(collection.find({}, {"_id": 0}))

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.warning("No Records Found")

# Search Student
elif menu == "Search Student":

    st.subheader("Search Student")

    roll = st.text_input("Enter Roll Number")

    if st.button("Search"):

        student = collection.find_one(
            {"roll": roll},
            {"_id": 0}
        )

        if student:
            st.write(student)
        else:
            st.error("Student Not Found")

# Delete Student
elif menu == "Delete Student":

    st.subheader("Delete Student")

    roll = st.text_input("Enter Roll Number to Delete")

    if st.button("Delete"):

        result = collection.delete_one({"roll": roll})

        if result.deleted_count:
            st.success("Student Deleted Successfully")
        else:
            st.error("Student Not Found")
