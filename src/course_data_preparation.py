import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from tqdm import tqdm  


departments = {
    2: ['engineering', 'development', 'software', 'coding'],
    3: ['product', 'management', 'strategy'],
    4: ['quality', 'assurance', 'testing'],
    5: ['information', 'technology', 'IT', 'support'],
    6: ['data', 'science', 'analytics', 'statistics'],
    7: ['devops', 'development', 'operations', 'cloud', 'version control'],
    8: ['cybersecurity', 'security', 'hacking', 'penetration testing'],
    9: ['user interface', 'user experience', 'design', 'UI', 'UX'],
    10: ['sales', 'selling', 'marketing'],
    11: ['marketing', 'advertising', 'branding', 'ads'],
    12: ['customer', 'support', 'success', 'marketing'],
    13: ['human resources', 'HR', 'recruitment'],
    14: ['finance', 'financial', 'accounting', 'economics'],
    15: ['legal', 'compliance', 'law', 'history']
}

def course_preperation(df, threshold=0.09):
    department_assignments = []
    department_counts = {dept_id: 0 for dept_id in departments.keys()}  

    vectorizer = TfidfVectorizer()

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Classifying Courses"):
        course_text = f"{row['course_name']} {row['course_desc']} {' '.join(row['skills'].split(','))}"
        
        course_vector = vectorizer.fit_transform([course_text])
        
        department_scores = {}

        for dept_id, keywords in departments.items():
            dept_keywords = ' '.join(keywords)

            dept_vector = vectorizer.transform([dept_keywords])
            
            
            similarity = cosine_similarity(course_vector, dept_vector)[0][0]
            department_scores[dept_id] = similarity

        assigned_departments = [dept for dept, score in department_scores.items() if score > threshold]
        department_assignments.append(assigned_departments)

        for dept in assigned_departments:
            department_counts[dept] += 1

    df['assigned_departments'] = department_assignments

    courses_with_depts = sum(1 for depts in department_assignments if len(depts) > 0)
    print(f"Number of courses with at least one department assigned: {courses_with_depts}")
    
    
    dept_assignment_counts = [department_counts[dept_id] for dept_id in departments.keys()]
    print(f"Department assignment counts: {dept_assignment_counts}")

    return dept_assignment_counts

input_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'extracted_courses.csv')  
df_courses = pd.read_csv(input_csv_path)

dept_assignment_counts = course_preperation(df_courses)

output_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'classified_courses.csv')
df_courses.to_csv(output_csv_path, index=False)

print(f"Classified courses saved to {output_csv_path}")
