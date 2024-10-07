import pandas as pd
import random
import os
import ast
from tqdm import tqdm  


def process_course_data(input_classified_courses, input_user_data):
    """
    Process course data to generate two DataFrames: one with course details and another with 
    course-department mappings. Assigns images and random course creators for each course.

    Args:
        input_classified_courses (str): Path to the classified courses CSV.
        input_user_data (str): Path to the user data CSV.

    Returns:
        df_courses_output (pd.DataFrame): Contains course_id, course_name, course_desc, course_img, course_creator.
        df_course_dept (pd.DataFrame): Contains course_id, dept_id (mapping courses to departments).
    """
    images_with_dept_id = {
        2: 'https://images.pexels.com/photos/577585/pexels-photo-577585.jpeg',
        3: 'https://images.pexels.com/photos/669619/pexels-photo-669619.jpeg',
        4: 'https://images.pexels.com/photos/3862132/pexels-photo-3862132.jpeg',
        5: 'https://images.pexels.com/photos/1181675/pexels-photo-1181675.jpeg',
        6: 'https://images.pexels.com/photos/265087/pexels-photo-265087.jpeg',
        7: 'https://images.pexels.com/photos/11035393/pexels-photo-11035393.jpeg',
        8: 'https://images.pexels.com/photos/5483240/pexels-photo-5483240.jpeg',
        9: 'https://images.pexels.com/photos/196644/pexels-photo-196644.jpeg',
        10: 'https://images.pexels.com/photos/12935051/pexels-photo-12935051.jpeg',
        11: 'https://images.pexels.com/photos/267401/pexels-photo-267401.jpeg',
        12: 'https://images.pexels.com/photos/8867382/pexels-photo-8867382.jpeg',
        13: 'https://images.pexels.com/photos/4344860/pexels-photo-4344860.jpeg',
        14: 'https://images.pexels.com/photos/128867/coins-currency-investment-insurance-128867.jpeg',
        15: 'https://images.pexels.com/photos/5668473/pexels-photo-5668473.jpeg',
    }

    df_courses = pd.read_csv(input_classified_courses)
    df_users = pd.read_csv(input_user_data)

    # Get all admin user_ids
    admin_user_ids = df_users[df_users['account_type'] == 'admin']['user_id'].tolist()

    def convert_to_list(department_str):
        if isinstance(department_str, str):
            return ast.literal_eval(department_str)
        return department_str  
    
    df_courses['assigned_departments'] = df_courses['assigned_departments'].apply(convert_to_list)
    df_filtered_courses = df_courses[df_courses['assigned_departments'].apply(len) > 0].copy()
    
    df_filtered_courses['course_id'] = range(1, len(df_filtered_courses) + 1)  

    # Function to assign a random image based on assigned departments
    def assign_random_image(departments):
        return images_with_dept_id[random.choice(departments)]

    tqdm.pandas(desc="Assigning Images and Creators") 
    df_filtered_courses['course_name'] = df_filtered_courses['course_name'].str.strip()
    df_filtered_courses['course_desc'] = df_filtered_courses['course_desc'].str.strip()

    df_filtered_courses['course_img'] = df_filtered_courses['assigned_departments'].progress_apply(assign_random_image)
    df_filtered_courses['course_creator'] = df_filtered_courses['assigned_departments'].apply(lambda _: random.choice(admin_user_ids))

    # Create the first DataFrame with course details
    df_courses_output = df_filtered_courses[['course_id', 'course_name', 'course_desc', 'course_img', 'course_creator']]

    # Create the second DataFrame (course_id, dept_id mapping)
    df_course_dept = df_filtered_courses.explode('assigned_departments')[['course_id', 'assigned_departments']]
    df_course_dept.columns = ['course_id', 'dept_id']  

    return df_courses_output, df_course_dept


# Input CSVs
input_classified_courses = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'classified_courses.csv')
input_user_data = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'user_data_with_hash.csv')

df_courses_output, df_course_dept = process_course_data(input_classified_courses, input_user_data)

# Course Data
output_courses_csv = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Course.csv')
df_courses_output.to_csv(output_courses_csv, index=False)

# CourseDepartment Data
output_dept_csv = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'CourseDepartment.csv')
df_course_dept.to_csv(output_dept_csv, index=False)

# Print file paths for verification
print(f"Course details saved to {output_courses_csv}")
print(f"Course to department mappings saved to {output_dept_csv}")
