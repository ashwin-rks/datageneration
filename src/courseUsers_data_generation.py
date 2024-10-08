import pandas as pd
import random
import os
from datetime import datetime
from tqdm import tqdm 


def generate_course_users(user_data_path, course_department_path):
    
    # CSVs
    user_data_df = pd.read_csv(user_data_path)
    course_department_df = pd.read_csv(course_department_path)

    # Dates
    start_date = datetime(2019, 3, 28)
    end_date = datetime(2021, 6, 10)
    current_date = datetime(2021, 6, 10)

    # Modifing User.csv
    user_data_df['createdAt'] = pd.to_datetime(user_data_df['createdAt'])
    filtered_users = user_data_df[(user_data_df['createdAt'] >= start_date) & (user_data_df['createdAt'] <= end_date)]
    filtered_users['account_age_days'] = (current_date - filtered_users['createdAt']).dt.days
    user_data = filtered_users[['user_id', 'dept_id', 'account_age_days']]

    # Mergeing CSVs
    merged_course_df = pd.merge(user_data, course_department_df, on='dept_id', how='left')
    user_courses = merged_course_df.groupby('user_id')['course_id'].apply(lambda x: [int(c) for c in x if pd.notna(c)]).reset_index()
    user_data = pd.merge(user_data, user_courses, on='user_id', how='left')
    user_data['course_id'] = user_data['course_id'].apply(lambda x: [] if len(x) == 0 or pd.isna(x).any() else x)

    def get_score(account_age_days):
        if account_age_days <= 200:
            return random.randint(40, 70)
        elif 201 <= account_age_days <= 500:
            return random.randint(50, 80)
        elif 501 <= account_age_days <= 700:
            return random.randint(60, 100)
        elif 701 <= account_age_days <= 1000:
            return random.randint(75, 100)

    def get_num_courses(course_ids, account_age_days):
        if len(course_ids) == 0:
            return 0  

        if account_age_days <= 200:
            return max(1, random.randint(1, int(len(course_ids) * 0.4)))
        elif 201 <= account_age_days <= 500:
            return random.randint(int(len(course_ids) * 0.2), int(len(course_ids) * 0.6))
        elif 501 <= account_age_days <= 700:
            return random.randint(int(len(course_ids) * 0.5), int(len(course_ids) * 0.8))
        else:
            return random.randint(int(len(course_ids) * 0.7), len(course_ids))

    course_users_df = pd.DataFrame(columns=['course_id', 'user_id', 'score'])

    for user_index, user_row in tqdm(user_data.iterrows(), total=user_data.shape[0], desc="Generating courses for users"):
        user_id = user_row['user_id']
        account_age_days = user_row['account_age_days']
        course_ids = user_row['course_id']

        if len(course_ids) > 0:  
            num_courses = get_num_courses(course_ids, account_age_days)
            assigned_courses = random.sample(course_ids, num_courses)

            new_entries = []
            for course in assigned_courses:
                score = get_score(account_age_days)
                new_entries.append({
                    'course_id': course,
                    'user_id': user_id,
                    'score': score
                })

            course_users_df = pd.concat([course_users_df, pd.DataFrame(new_entries)], ignore_index=True)

    course_users_df['id'] = range(1, len(course_users_df) + 1)
    course_users_df = course_users_df[['id', 'user_id', 'course_id', 'score']]


    return course_users_df


user_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'User.csv')
course_department_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'CourseDepartment.csv')

course_users_df = generate_course_users(user_data_path, course_department_path)
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'CourseUser.csv')
course_users_df.to_csv(output_path, index=False)
print(f'Stored CourseUsers.csv at : {os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'CourseUser.csv')}')
