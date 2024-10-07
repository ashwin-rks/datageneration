import pandas as pd
import os

def process_courses(input_csv, output_csv, skills_file):
    """
    Process the courses from the input CSV and create a new CSV with selected fields
    and a text file with unique skills.

    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to the output CSV file.
        skills_file (str): Path to the output text file for unique skills.
    """
    # Read the input CSV file
    df = pd.read_csv(input_csv)
    df.columns = df.columns.str.strip()
    print("Cleaned column names:", df.columns.tolist())

    # Select the desired columns
    df_filtered = df[['Course Name', 'Course URL', 'Course Description', 'Skills']].copy()
    df_filtered.columns = ['course_name', 'course_url', 'course_desc', 'skills']

    # Gather unique skills
    unique_skills = set()
    for skills in df_filtered['skills']:
        # Split skills by comma and strip whitespace
        if isinstance(skills, str):  # Check if skills is a string
            skills_list = [skill.strip() for skill in skills.split(',')]
            unique_skills.update(skills_list)

    # Write the filtered DataFrame to a new CSV
    df_filtered.to_csv(output_csv, index=False)

    # Write unique skills to a text file
    with open(skills_file, 'w', encoding='utf-8') as f:
        for skill in unique_skills:
            f.write(skill + '\n')

    print(f"Processed courses saved to {output_csv}")
    print(f"Unique skills saved to {skills_file}")

# Define file paths
input_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Coursera.csv')  
output_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed_courses.csv')
skills_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'unique_skills.txt')


process_courses(input_csv_path, output_csv_path, skills_file_path)
