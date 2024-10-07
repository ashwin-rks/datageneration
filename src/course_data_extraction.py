import pandas as pd
import os

def course_extraction(input_csv, output_csv):
    """
    Process the courses from the input CSV and create a new CSV with selected fields
    and a text file with unique skills.

    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to the output CSV file.
        skills_file (str): Path to the output text file for unique skills.
    """
    print(f"Extracting Courses ---> ")
    df = pd.read_csv(input_csv)
    df.columns = df.columns.str.strip()
    print("Cleaned column names:", df.columns.tolist())

    df_filtered = df[['Course Name', 'Course URL', 'Course Description', 'Skills']].copy()
    df_filtered.columns = ['course_name', 'course_url', 'course_desc', 'skills']
    df_filtered['course_id'] = range(1, len(df_filtered) + 1)
    df_filtered = df_filtered[['course_id', 'course_name', 'course_url', 'course_desc', 'skills']]

    df_filtered.to_csv(output_csv, index=False)

    print(f"Processed courses saved to {output_csv}")

input_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Coursera.csv')  
output_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'extracted_courses.csv')

course_extraction(input_csv_path, output_csv_path)
