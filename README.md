# Python Data Generation Project

This project is designed to generate various datasets for my [webapp](https://github.com/ashwin-rks/webapp). It utilizes Python and several libraries to handle data generation tasks efficiently.

## Prerequisites

- **Python**: Version 3.12.5 or higher

## Setup Instructions

Follow these steps to set up the project on your local machine:

1. **Create a virtual environment**:
   ```bash
   virtualenv venv
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the main script**:
   ```bash
   python main.py
   ```

## Project Structure

```
project-directory/
│
├── src/                     # Source files for data generation
│   ├── user_data_generate.py
│   ├── course_data_extraction.py
│   ├── course_data_preparation.py
│   ├── course_data_generation.py
│   ├── skill_data_generation.py
│   ├── skillUsers_data_generation.py
│   └── courseUsers_data_generation.py
│
├── data/                    # Directory for input/output CSV files (files present are required to run)
│   ├── Coursera.csv
│   ├── Department.csv
│   └── extracted_skills.csv
│
├── requirements.txt         # List of Python packages required
└── main.py                  # Main script to run the project
```
