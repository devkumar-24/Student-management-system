import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB Connection
client = MongoClient("mongodb+srv://devkumar82986_db_user:Dev@89866@cluster0.sof4suw.mongodb.net/?appName=Cluster0")
db = client["student_db"]
collection = db["students"]

st.title("🎓 Student Management System")

menu = ["Add Student", "View Students", "Search Student", "Delete Student"]
choice = st.sidebar.selectbox("Menu", menu)

# Add Student
if choice == "Add Student":

    st.subheader("Add Student")

    sid = st.text_input("Student ID")
    name = st.text_input("Name")
    course = st.selectbox(
        "Course",
        ["BCA", "BBA", "MCA", "MBA", "B.Tech"]
    )
    marks = st.number_input(
        "Marks",
        min_value=0,
        max_value=100
    )

    if st.button("Add Student"):

        data = {
            "Student ID": sid,
            "Name": name,
            "Course": course,
            "Marks": marks
        }

        collection.insert_one(data)
        st.success("Student Added Successfully!")

# View Students
elif choice == "View Students":

    st.subheader("Student Records")

    students = list(collection.find({}, {"_id": 0}))

    if students:
        df = pd.DataFrame(students)
        st.dataframe(df)
    else:
        st.warning("No Records Found")

# Search Student
elif choice == "Search Student":

    st.subheader("Search Student")

    sid = st.text_input("Enter Student ID")

    if st.button("Search"):

        student = collection.find_one(
            {"Student ID": sid},
            {"_id": 0}
        )

        if student:
            st.json(student)
        else:
            st.error("Student Not Found")

# Delete Student
elif choice == "Delete Student":

    st.subheader("Delete Student")

    sid = st.text_input("Enter Student ID to Delete")

    if st.button("Delete"):

        result = collection.delete_one(
            {"Student ID": sid}
        )

        if result.deleted_count:
            st.success("Student Deleted")
        else:
            st.error("Student Not Found")
