import os
import pandas as pd
import random
from datetime import datetime
from tqdm import tqdm 

def generate_skillUsers(user_data_path, skill_department_path):
    
    skill_department_df = pd.read_csv(skill_department_path)
    user_data_df = pd.read_csv(user_data_path)

    start_date = datetime(2019, 3, 28)
    end_date = datetime(2021, 6, 10)
    current_date = datetime(2021, 6, 10)

    user_data_df['createdAt'] = pd.to_datetime(user_data_df['createdAt'])
    filtered_users = user_data_df[(user_data_df['createdAt'] >= start_date) & (user_data_df['createdAt'] <= end_date)]
    filtered_users['account_age_days'] = (current_date - filtered_users['createdAt']).dt.days
    user_data = filtered_users[['user_id', 'dept_id', 'account_age_days']]

    merged_df = pd.merge(user_data, skill_department_df, on='dept_id', how='left')
    user_skills = merged_df.groupby('user_id')['skill_id'].apply(lambda x: [int(s) for s in x if pd.notna(s)]).reset_index()
    user_data = pd.merge(user_data, user_skills, on='user_id', how='left')
    user_data['skill_id'] = user_data['skill_id'].apply(lambda x: [] if len(x) == 0 or pd.isna(x).any() else x)

    def get_competency(account_age_days):
        if account_age_days <= 200:
            competencies = ['beginner'] * 3 + ['intermediate'] * 1
        elif 201 <= account_age_days <= 500:
            competencies = ['beginner'] * 2 + ['intermediate'] * 3 + ['advanced'] * 1
        elif 501 <= account_age_days <= 700:
            competencies = ['intermediate'] * 1 + ['advanced'] * 2
        elif 701 <= account_age_days <= 1000:
            competencies = ['intermediate'] * 1 + ['advanced'] * 4
        return random.choice(competencies)

    def get_num_skills(skill_ids, account_age_days):
        if len(skill_ids) == 0:
            return 0  
        
        if account_age_days <= 200:
            return max(1, random.randint(1, int(len(skill_ids) * 0.4)))
        elif 201 <= account_age_days <= 500:
            return random.randint(int(len(skill_ids) * 0.2), int(len(skill_ids) * 0.6))
        elif 501 <= account_age_days <= 700:
            return random.randint(int(len(skill_ids) * 0.5), int(len(skill_ids) * 0.8))
        else:
            return random.randint(int(len(skill_ids) * 0.7), len(skill_ids))

    skill_users_df = pd.DataFrame(columns=['id', 'skill_id', 'user_id', 'competency'])

    for user_index, user_row in tqdm(user_data.iterrows(), total=user_data.shape[0], desc="Generating skills for users"):
        user_id = user_row['user_id']
        account_age_days = user_row['account_age_days']
        skill_ids = user_row['skill_id']

        if len(skill_ids) > 0:  
            num_skills = get_num_skills(skill_ids, account_age_days)
            assigned_skills = random.sample(skill_ids, num_skills)

            new_entries = []
            for skill in assigned_skills:
                competency = get_competency(account_age_days)
                new_entries.append({
                    'id': len(skill_users_df) + 1,  
                    'skill_id': skill,
                    'user_id': user_id,
                    'competency': competency
                })

            skill_users_df = pd.concat([skill_users_df, pd.DataFrame(new_entries)], ignore_index=True)

    return skill_users_df

user_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'User.csv')
skill_department_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'SkillDepartment.csv')

skill_users_df = generate_skillUsers(user_data_path, skill_department_path)
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'SkillUsers.csv')
skill_users_df.to_csv(output_path, index=False)
print(f'Stored SkillUsers.csv at : {os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'SkillUsers.csv')}')
