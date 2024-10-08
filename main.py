import os
import sys
import pandas as pd
from colorama import Fore, Style

sys.path.append(os.path.join(os.getcwd(), 'src'))

from user_data_generate import generate_user_data
from course_data_extraction import course_extraction
from course_data_preparation import course_preperation
from course_data_generation import course_generation
from skill_data_generation import create_skill_and_dept_csvs
from skillUsers_data_generation import generate_skillUsers
from courseUsers_data_generation import generate_course_users

def main():
    generate_user_data(800)

    # For course extraction need coursera csv
    input_csv_path = os.path.join(os.getcwd(), 'data', 'Coursera.csv')  
    output_csv_path = os.path.join(os.getcwd(), 'data', 'extracted_courses.csv')
    course_extraction(input_csv_path, output_csv_path)

    # For course preparation
    input_csv_path = os.path.join(os.getcwd(), 'data', 'extracted_courses.csv')  
    df_courses = pd.read_csv(input_csv_path)

    dept_assignment_counts = course_preperation(df_courses)

    output_csv_path = os.path.join(os.getcwd(), 'data', 'classified_courses.csv')
    df_courses.to_csv(output_csv_path, index=False)

    print(f"{Fore.GREEN}Classified courses saved to {output_csv_path}{Style.RESET_ALL}")

    # For Course Data generation
    input_classified_courses = os.path.join(os.getcwd(), 'data', 'classified_courses.csv')
    input_user_data = os.path.join(os.getcwd(), 'data', 'User.csv')

    df_courses_output, df_course_dept = course_generation(input_classified_courses, input_user_data)

    output_courses_csv = os.path.join(os.getcwd(), 'data', 'Course.csv')
    df_courses_output.to_csv(output_courses_csv, index=False)

    output_dept_csv = os.path.join(os.getcwd(), 'data', 'CourseDepartment.csv')
    df_course_dept.to_csv(output_dept_csv, index=False)

    print(f"{Fore.GREEN}Course details saved to {output_courses_csv}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Course to department mappings saved to {output_dept_csv}{Style.RESET_ALL}")

    # Create skills
    input_file = os.path.join(os.getcwd(), 'data', 'extracted_skills.csv')
    output_dir = os.path.join(os.getcwd(), 'data')

    create_skill_and_dept_csvs(input_file, output_dir)

    # Create skill users
    user_data_path = os.path.join(os.getcwd(), 'data', 'User.csv')
    skill_department_path = os.path.join(os.getcwd(), 'data', 'SkillDepartment.csv')

    skill_users_df = generate_skillUsers(user_data_path, skill_department_path)
    output_path = os.path.join(os.getcwd(), 'data', 'SkillUsers.csv')
    skill_users_df.to_csv(output_path, index=False)
    print(f"{Fore.GREEN}Stored SkillUsers.csv at : {output_path}{Style.RESET_ALL}")

    # Create course users
    user_data_path = os.path.join(os.getcwd(), 'data', 'User.csv')
    course_department_path = os.path.join(os.getcwd(), 'data', 'CourseDepartment.csv')

    course_users_df = generate_course_users(user_data_path, course_department_path)
    output_path = os.path.join(os.getcwd(), 'data', 'CourseUser.csv')
    course_users_df.to_csv(output_path, index=False)
    print(f"{Fore.GREEN}Stored CourseUsers.csv at : {output_path}{Style.RESET_ALL}")

    print(f"{Fore.GREEN}Created all CSVs{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
