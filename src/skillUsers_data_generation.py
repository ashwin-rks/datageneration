import pandas as pd
import random
import os
from datetime import datetime
from tqdm import tqdm  

def create_skill_users(user_data_path, skill_department_path):
    """
    Creates a CSV file 'SkillUsers.csv' that maps users to their skills 
    based on their department and account age. 

    The function processes user data to filter users who created their 
    accounts between October 1, 2020, and October 7, 2020. For each user, 
    it identifies associated skills from the SkillDepartment data based 
    on the user's department. The competency level for each skill is 
    assigned based on the age of the user's account, with more mature 
    accounts likely having higher competency levels.

    Parameters:
    user_data_path (str): The file path to the CSV file containing user data 
                           including 'user_id', 'dept_id', and 'createdAt'.
    skill_department_path (str): The file path to the CSV file containing 
                                 skills and their associated departments 
                                 including 'skill_id' and 'dept_id'.

    Output:
    A CSV file named 'SkillUsers.csv' is created in the current working 
    directory. The file contains the following columns:
        - id (int): Unique identifier for each skill-user assignment.
        - user_id (int): The ID of the user associated with the skill.
        - skill_id (int): The ID of the skill assigned to the user.
        - competency (str): The competency level assigned to the user for 
                            the skill. Possible values are 'beginner', 
                            'intermediate', or 'advanced'.
    """
    skill_department_df = pd.read_csv(skill_department_path)
    user_data_df = pd.read_csv(user_data_path)


    user_data_df['createdAt'] = pd.to_datetime(user_data_df['createdAt'])
    start_date = datetime(2020, 10, 1)
    end_date = datetime(2024, 10, 7)
    filtered_users = user_data_df[(user_data_df['createdAt'] >= start_date) & (user_data_df['createdAt'] <= end_date)]
    
    skill_user_counter = 1
    skill_users_data = []
    current_date = datetime(2020, 10, 7)

    def assign_competency(created_at):
        account_age_days = (current_date - created_at).days
        if account_age_days <= 200:
            competencies = ['beginner'] * 3 + ['intermediate'] * 1
        elif 201 <= account_age_days <= 500:
            competencies = ['beginner'] * 2 + ['intermediate'] * 3 + ['advanced'] * 1
        elif 501 <= account_age_days <= 700:
            competencies = ['intermediate'] * 1 + ['advanced'] * 2
        elif 701 <= account_age_days <= 1000:
            competencies = ['intermediate'] * 1 + ['advanced'] * 4
        return random.choice(competencies)

    for _, user in tqdm(filtered_users.iterrows(), total=filtered_users.shape[0], desc='Processing Users'):
        user_id = user['user_id']
        dept_id = user['dept_id']
        created_at = user['createdAt']
        user_skills = skill_department_df[skill_department_df['dept_id'] == dept_id]

        if (created_at >= current_date - pd.Timedelta(days=1000)) and not user_skills.empty:
            days_old = (current_date - created_at).days
            
            if days_old <= 200:
                num_skills = max(1, random.randint(1, int(len(user_skills) * 0.4)))
            elif 201 <= days_old <= 500:
                num_skills = random.randint(int(len(user_skills) * 0.2), int(len(user_skills) * 0.6))
            elif 501 <= days_old <= 700:
                num_skills = random.randint(int(len(user_skills) * 0.5), int(len(user_skills) * 0.8))
            else:  
                num_skills = random.randint(int(len(user_skills) * 0.7), int(len(user_skills)))

            assigned_skills = user_skills.sample(n=num_skills)

            for _, skill in assigned_skills.iterrows():
                skill_id = skill['skill_id']
                competency = assign_competency(created_at)
                skill_users_data.append([skill_user_counter, user_id, skill_id, competency])
                skill_user_counter += 1

    skill_users_df = pd.DataFrame(skill_users_data, columns=['id', 'user_id', 'skill_id', 'competency'])
    output_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__))), 'data', 'SkillUsers.csv')
    skill_users_df.to_csv(output_path, index=False)

    print("SkillUsers.csv created successfully!")

user_data_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__))), 'data', 'User.csv')
skillDepartment_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__))), 'data', 'SkillDepartment.csv')

create_skill_users(user_data_path, skillDepartment_path)
