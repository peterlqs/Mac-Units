import streamlit as st
import pandas as pd
import ast
import numpy as np
import math

st.set_page_config(layout="wide")

df_degree = pd.read_excel("course_data3.xlsx")
if "selected_course_code" not in st.session_state:
    st.session_state.selected_course_code = ""
if "name" not in st.session_state:
    st.session_state.name = ""

st.title("Degree Lookup")

# Input field for course name
course_name_degree = st.text_input("Enter the degree:", value=st.session_state.name)

df2 = df_degree[df_degree["Degree"].str.lower() == course_name_degree.strip().lower()]
# Create an empty dictionary
if not df2.empty:
    category_dict = {}

    # Iterate over the DataFrame and populate the dictionary
    for _, row in df2.iterrows():
        category = row["Category"]
        course_code = row["Course Code"]
        course_name_degree = row["Course Name"]

        if category not in category_dict:
            category_dict[category] = []

        category_dict[category].append((course_code, course_name_degree))

    # Print the dictionary
    # Iterate over the dictionary and display the course information
    st.markdown(
        """
            <style>
            button {
                background: none!important;
                border: none;
                padding: 0 5px!important;
                color: black !important;
                text-decoration: none;
                cursor: pointer;
                border: none !important;
            }
            button:hover {
                text-decoration: none;
                color: black !important;
            }
            button:focus {
                outline: none !important;
                box-shadow: none !important;
                color: black !important;
            }
            </style>
            """,
        unsafe_allow_html=True,
    )
    for category, courses in category_dict.items():
        st.markdown(f"**{category}**")

        # Split the output into two columns
        col1, col2 = st.columns(2)

        # Iterate over the courses and display them in the columns
        for i, course in enumerate(courses):
            course_code, course_name_degree = course

            # Alternate between columns for each course

            if i % 2 == 0:
                with col1:
                    if st.button(
                        f"{course_code} - {course_name_degree}",
                        key=f"button_{course_code}",
                        # help=course_code,
                    ):
                        if category == "Major":
                            st.session_state["name"] = course_name_degree
                        else:
                            st.session_state["selected_course_code"] = course_code
                        # pass  # Placeholder to prevent immediate execution
            else:
                with col2:
                    if st.button(
                        f"{course_code} - {course_name_degree}",
                        key=f"button_{course_code}",
                        # help=course_code,
                    ):
                        if category == "Major":
                            st.session_state["name"] = course_name_degree
                        else:
                            st.session_state["selected_course_code"] = course_code

                        # pass  # Placeholder to prevent immediate execution
else:
    st.write("No matching degree found.")

## UNIT

df_all = pd.read_excel("final_merged_data.xlsx")

# Create a Streamlit app
st.title("Course Information Lookup")

# Input field for course name

course_name = (
    st.text_input(
        "Enter the Course Code:",
        value=st.session_state.selected_course_code,
    )
    .upper()
    .strip()
)


# Filter the DataFrame based on the entered course name
df = df_all[df_all["Course Code"] == course_name]

# Display the selected columns vertically
if not df.empty:
    course_code = df["Course Code"].values[0]
    course_name = df["Course Name"].values[0]
    major = df["Major"].values[0]
    prerequisites = df["Prerequisites"].values[0]
    period = df["Period"].values[0]
    reviews = df["Reviews"].values[0]
    star = df["Star"].values[0]
    link = df["Link"].values[0]
    corequisites = df["Corequisites"].values[0]
    co_badged_units = df["Co-badged Units"].values[0]
    description = df["Description"].values[0]
    final_exam = df["Final Exam"].values[0]
    teamwork = df["Teamwork"].values[0]
    assignment_type = df["Assignment type"].values[0]
    unit_date = df["Unit Date"].values[0]

    st.divider()
    header = f"<h2 style='text-align: center;'>{course_code} - {course_name}</h2>"
    st.markdown(header, unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Description:**\n\n{description}")
        if str(star) != "nan":
            stars = "★" * int(star)
            st.write("**Rating on StudentVIP:**", stars)
        st.write("**Reviews:**")
        if str(reviews) != "nan" and str(reviews) != "[]":
            for m in ast.literal_eval(reviews):
                st.write("- ", m)

    with col2:
        st.write("**Unit Link:**", link)
        st.write(
            "**Handbook Link:**",
            f"https://coursehandbook.mq.edu.au/2023/units/{course_code}",
        )

        st.write("**Prerequisites:**", prerequisites)
        st.write("**Corequisites:**", corequisites)
        st.write("**Co-badged Units:**", co_badged_units)
        st.write("**Final Exam:**", final_exam)
        if teamwork == "No":
            teamwork = "Possibly no"
        st.write("**Teamwork:**", teamwork)
        st.write("**Assignment type:**")
        for m in ast.literal_eval(assignment_type):
            st.write("- ", m)
        st.write("**Found in these degree(s)/major(s):**")
        for m in ast.literal_eval(major):
            st.write("- ", m)
        st.write("**Offering:**")
        period = str(period.split("\n"))
        for m in ast.literal_eval(period):
            st.write("- ", m)
        st.write("**Info from this session:**", unit_date)


else:
    st.write("No matching course found.")
