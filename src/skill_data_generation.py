import os
import pandas as pd

def create_skill_and_dept_csvs(input_file_path: str, output_dir: str):
    """
    Creates two CSVs from the input file: Skill.csv with skill_id and skill_name,
    and SkillDepartment.csv with skill_id, dept_id, and an id counter.
    
    Args:
    input_file_path (str): Path to the input CSV file.
    output_dir (str): Directory where the output CSVs will be saved.
    """

    print(f'Generating Skill Data')
    # Read the input CSV file
    df = pd.read_csv(input_file_path)
    
    # Enclose dept_ids in quotes in the original dataframe before any processing
    df['dept_ids'] = df['dept_ids'].apply(lambda x: f'"{x}"')
    
    # Create Skill.csv with skill_id and skill_name
    df[['skill_id', 'skill_name']].to_csv(os.path.join(output_dir, 'Skill.csv'), index=False)
    
    # Exploding dept_ids and saving to SkillDepartment.csv with a counter 'id'
    df['dept_ids'] = df['dept_ids'].str.strip('[]"').str.split(', ')  # Remove brackets and split into list
    df_exploded = df[['skill_id', 'dept_ids']].explode('dept_ids')
    df_exploded.rename(columns={'dept_ids': 'dept_id'}, inplace=True)
    
    # Add an id column that increments as a counter
    df_exploded['id'] = range(1, len(df_exploded) + 1)
    
    # Reorder columns to have 'id', 'skill_id', and 'dept_id'
    df_exploded = df_exploded[['id', 'skill_id', 'dept_id']]
    
    # Save to SkillDepartment.csv
    df_exploded.to_csv(os.path.join(output_dir, 'SkillDepartment.csv'), index=False)
    print(f'Skill Data generated and stroed at {os.path.join(output_dir, 'SkillDepartment.csv')}')



# input_file = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__))), 'data', 'extracted_skills.csv')
# output_dir = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__))), 'data')

# create_skill_and_dept_csvs(input_file, output_dir)
