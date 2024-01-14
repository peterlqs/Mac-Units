import random
import streamlit as st
import pandas as pd
import ast
import numpy as np
import math

st.set_page_config(
    page_title="Unit Lookup",
    layout="wide",
)
course_units = pd.read_csv("data/course_units.csv")
if "selected_course_code" not in st.session_state:
    st.session_state.selected_course_code = ""
if "back_to_selected_course" not in st.session_state:
    st.session_state.back_to_selected_course = ""
if "name" not in st.session_state:
    st.session_state.name = ""

st.title("Degree Lookup")

# Input field for course name
course_name = st.text_input(
    "Enter the Degree/Major:", value=st.session_state.name
)
# Preset (ex: BIT -> Bachelor of Information Technology)
course_mapping = {
    "bit": "bachelor of information technology",
    "ba": "bachelor of arts",
    "bcom": "bachelor of commerce",
    "bsc": "bachelor of science",
    "bb": "bachelor of business",
    # Add more mappings as needed
}
course_name = course_mapping.get(course_name.lower(), course_name)

# Because the course_name in course_units is not all lower/upper
def convert_case(sentence):
    # Define a list of words to be converted to lowercase
    lowercase_words = ['a', 'an', 'the', 'of', 'and', 'in']
    # Split the sentence into words
    words = sentence.split()
    # Process each word
    processed_words = [word.lower() if word.lower() in lowercase_words else word.capitalize() for word in words]
    # Join the processed words back into a sentence
    processed_sentence = ' '.join(processed_words)
    return processed_sentence

# Back to the selected course
if st.session_state.back_to_selected_course:
    if st.button(f"Back to: {convert_case(st.session_state.back_to_selected_course)}"):
        st.session_state.name = st.session_state.back_to_selected_course
        # Hide button
        st.session_state.back_to_selected_course = ""
        st.rerun()  


# Output
if course_name:
    col1, col2 = st.columns(2)
    # Get all units from unit_code + unit_name, group by unit_category where course_name = course_name, put it in a dict
    course_units_filtered = course_units[course_units["course_name"] == convert_case(course_name)]
    # If not found with course name then try with course_code
    if len(course_units_filtered) == 0:
        course_units_filtered = course_units[course_units["course_code"] == course_name.upper()]
    # Shows error if no results
    if len(course_units_filtered) == 0:
        st.write(f"No matching course found. Try major in {course_name}/specialisation in {course_name}/master in {course_name}/ bachelor in {course_name} instead.")
    # Loop through the df and display the unit_name by unit_category
    units_dict = {}
    for _, row in course_units_filtered.iterrows():
        units_dict[row["unit_category"]] = units_dict.get(row["unit_category"], []) + [row["unit_code"] + " - " + row["unit_name"]]
    # Sort by category so it's consistent for all units
    units_dict = dict(sorted(units_dict.items(), reverse=True))
    
    for category, units in units_dict.items():
        count = 0
        st.markdown(f"**{category}**")
        col1, col2, col3 = st.columns(3)
        for count, unit in enumerate(units):
            if count % 3 == 0:
                col = col1
            elif count % 3 == 1:
                col = col2
            else:
                col = col3
            with col:
                if st.button(unit):
                    if "major" in category.lower():
                        st.session_state.back_to_selected_course = course_name
                        st.session_state.name = f"Major in {unit.split(' - ')[1]}"
                    elif "specialisation" in category.lower():
                        st.session_state.back_to_selected_course = course_name
                        st.session_state.name = f"Specialisation in {unit.split(' - ')[1]}"
                    else:
                        st.session_state.selected_course_code = unit.split(" - ")[0]
                    # Scroll to Unit Section
                    st.markdown("""<script>document.getElementById('Unit').scrollIntoView();</script>""", unsafe_allow_html=True)
                    st.rerun()  
     
                    
        
## UNIT
            
# Create a Streamlit app
st.title("Course Information Lookup")

# Input field for course name
unit_input = st.text_input(
        "Enter the Course Code/Course Name:",
        value=st.session_state.selected_course_code,
    )



# Filter the DataFrame based on the entered course name

# Display the selected columns vertically
if unit_input:
    unit_info = pd.read_csv("data/unit_info.csv")
    # Get the unit info from unit_code
    filtered = unit_info[unit_info["unit_code"] == unit_input.upper()]
    # Try find by course name if no results
    if len(filtered) == 0:
        filtered = unit_info[unit_info["unit_name"] == convert_case(unit_input)]
    # Shows error if no results
    if len(filtered) == 0:
        st.write("No matching course found.")
        st.stop()
    filtered = filtered.iloc[0]
    # Get unit_code
    unit_name = filtered["unit_name"]
    unit_code = filtered["unit_code"]
    # Get the unitguide link
    unitguide_link = pd.read_csv("data/unitguide_link.csv")
    # Add null safety
    if unit_code.upper() not in unitguide_link["unit_code"].values:
        # unitguide_link = unitguide_link.append({"unit_code": unit_code.upper(), "unitguide_link": "Not found"}, ignore_index=True)
        unitguide_link = "Not Found"
    else:
        unitguide_link = unitguide_link[unitguide_link["unit_code"] == unit_code.upper()].iloc[0]['unitguide_link']
    # Get the rules
    rules = filtered['unit_rules']
    rules = ast.literal_eval(rules)
    # Get the exams
    exams = filtered['assessments']
    exams = ast.literal_eval(exams)
    # Other courses that also have this unit
    similar_courses = course_units.loc[course_units['unit_code'] == unit_code.upper()]
    similar_courses_list = []
    for _, row in similar_courses.iterrows():
        similar_courses_list.append(row['course_name'] + "({})".format(row['unit_category']))
    # Get the offerings
    all_offerings = unit_info[unit_info['unit_code'] == unit_code.upper()].iloc[0]['unit_period']
    all_offerings = ast.literal_eval(all_offerings)   
    # Get reviews and stars
    reviews = pd.read_excel("data/studentvip.xlsx")
    reviews = reviews[reviews['Course Code'] == unit_code.upper()]
    # add null safety
    if len(reviews) == 0:
        reviews = pd.DataFrame([{"Course Code": unit_code.upper(), "reviews": np.nan, "stars": np.nan}])
    if pd.isna(reviews.iloc[0]['reviews']):
        reviews = []
        stars = "Not found"
    else:
        # Get stars
        star = reviews.iloc[0]['stars']
        if str(star) != "nan":
            stars = "★" * int(star)
        reviews = ast.literal_eval(reviews.iloc[0]['reviews'])
        
    # Get desc
    description = filtered.get('description',"")
    
    # Get year
    year = filtered['year']


    st.divider()
    header = f"<h2 style='text-align: center;'>{unit_code} - {unit_name}</h2>"
    st.markdown(header, unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Description:**\n\n{description.replace('<p>', '').replace('</p>', '')}")
        st.write("**Rating on StudentVIP:**", stars)
          # Reviews
        st.write("**Reviews:**")
        for review in reviews:
            st.write("- ", review)
        # Has final exam?
        if filtered['has_final_exam'] == True:
            has_exam = "Possibly Yes"
        else: 
            has_exam = "Possibly No"
      

    with col2:
        st.write("**Unit Link:**", unitguide_link)
        st.write(
            "**Handbook Link:**",
            filtered['handbook_url'],
        )
        # The rules
        for category, rule in rules.items():
            all_units_of_rule = ""
            for value in rule:
                all_units_of_rule += value + ", "
            st.write(f"**{convert_case(category)}**", ": ", all_units_of_rule[:-2])
        # The exams
        st.write("**Exams:**")
        # st.write("  - **Final exam:** ", has_exam)
        for name, details in exams.items():
            # st.write("-", f"**{name}:**")
            if details != {}:
                st.write(f"""
                - {details["assessment_type"] + " - " + details["assessment_weight"]+"%"}
                    - {str(details.get("assessment_description", '')).replace('<p>', '').replace('</p>', '')}""")
            
        # Courses that also have this unit
        st.write("**Other courses that also have this unit:**")
        for course in similar_courses_list:
            st.write("-", course)
        # Offerings
        st.write("**Offering:**")
        for offering in all_offerings:
            st.write("-", offering)
        # Last updated
        st.write("**Last updated:**", year)
        
        # st.write("""
        #     - Bullet point 1
        #     - Bullet point 2
        #         - Nested bullet point 1
        #         - Nested bullet point 2
        #             - Further nested bullet point""")
        
else:
    st.write("No matching course found.")
