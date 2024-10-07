import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import os
import random
import bcrypt
from tqdm import tqdm  

fake = Faker()

def generate_user_data(no_of_users):
    """
    Generate a CSV file with fake user data and store it in the data folder.
    
    Args:
        no_of_users (int): The number of user entries to generate.

    The generated CSV will contain the following fields:
        - user_id: A counter starting from 1.
        - first_name: A randomly generated first name.
        - last_name: A randomly generated last name.
        - email: Email with format based on account type. Admin accounts have `admin@jamngroup.com`, 
                user accounts have `@jmangroup.com`.
        - password: A randomly generated 8-character string, hashed using bcrypt.
        - account_type: Either "user" or "admin". The first entry is always an admin, and the user-to-admin ratio is 100:1.
        - dept_id: Assigned based on account_type and specified user distribution.
        - createdAt: A timestamp between 1-Oct-2020 and 7-Oct-2024. The values will be strictly increasing and within 14 days of the previous entry.
        - updatedAt: A timestamp after createdAt, within the same date range.

    The output is saved to the `data/user_data_without_hash.csv` and `data/user_data_with_hash.csv`.
    """
    data = []
    password_data = []  
    user_to_admin_ratio = 100

    dept_distribution = {
        2: 20,
        3: 12,
        4: 5,
        5: 7,
        6: 6,
        7: 9,
        8: 9,
        9: 12,
        10: 8,
        11: 6,
        12: 3,
        13: 5,
        14: 6,
        15: 1
    }

    dept_list = []
    for dept_id, count in dept_distribution.items():
        dept_list.extend([dept_id] * count)
    
    start_date = datetime(2018, 10, 1)  
    end_date = datetime(2024, 10, 7)  

    created_at = fake.date_time_between(start_date=start_date, end_date=end_date)

    # Use tqdm to show progress
    for user_id in tqdm(range(1, no_of_users + 1), desc="Generating Users"):
        first_name = fake.first_name()
        last_name = fake.last_name()
        password = fake.password(length=8)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        if user_id == 1:
            account_type = "admin"
            email = f"{first_name.lower()}.{last_name.lower()}$admin@jmangroup.com"
            dept_id = 1 
        else:
            if user_id % user_to_admin_ratio == 0:
                account_type = "admin"
                email = f"{first_name.lower()}.{last_name.lower()}$admin@jmangroup.com"
                dept_id = 1  
            else:
                account_type = "user"
                email = f"{first_name.lower()}.{last_name.lower()}@jmangroup.com"
                if not dept_list:  
                    for dept_id, count in dept_distribution.items():
                        dept_list.extend([dept_id] * count)
                    random.shuffle(dept_list)  
                
                dept_id = dept_list.pop(0)

        max_created_at = created_at + timedelta(days=2)
        created_at = fake.date_time_between(start_date=created_at, end_date=max_created_at)

        updated_at = fake.date_time_between(start_date=created_at, end_date=end_date)

        data.append({
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password,  
            "account_type": account_type,
            "dept_id": dept_id,
            "createdAt": created_at,
            "updatedAt": updated_at
        })
        
        password_data.append({
            "user_id": user_id,
            "password": password  
        })

    df = pd.DataFrame(data)
    password_df = pd.DataFrame(password_data)

    output_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    csv_filename_with_hash = os.path.join(output_directory, "User.csv")
    df.to_csv(csv_filename_with_hash, index=False)

    csv_filename_plain = os.path.join(output_directory, "user_data_plain.csv")
    password_df.to_csv(csv_filename_plain, index=False)

    print(f"{csv_filename_with_hash} created with {no_of_users} entries.")
    print(f"{csv_filename_plain} created with {no_of_users} entries.")

generate_user_data(800)
