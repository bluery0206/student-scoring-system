# Student Scoring System

A Django-based web application for instructors to manage student scores and academic records offline.

Home:
![home](https://github.com/user-attachments/assets/5374e816-2549-45ab-ba51-3e344ffc6394)

Test View:
![test-view-01](https://github.com/user-attachments/assets/f6ceefc9-8365-41c5-949a-80623046418a)
![test-view-02](https://github.com/user-attachments/assets/31f5f602-bd50-4819-bf31-fb8c389baf15)

Student View
![student-view](https://github.com/user-attachments/assets/c826897e-9710-45c5-b131-02357994090d)


## Features
- Section Handling: Create sections to divide students
- Course Management: Create courses per sections
- Score Recording: Enter student performance in a test
- Responsive Interface: Build with Halfmoon CSS framework

## Stack
- **Backend**: Django 5.2
- **Frontend**: Halfmoon CSS
- **Database**: SQLite (Django's Default)
- **Authentication**: Django's built-in auth sytem

## Installation

1. Clone the repository:
``` bash
git clone https://github.com/bluery0206/student-scoring-system.git
```

2. Create virtual environment:
``` bash
python -m venv venv
```
   If it doesn't work, try replacing `python` with `py`, or `python3`.

3. Activate the virtual environment:
``` bash
# for Windows
venv\scripts\activate
```
``` bash
# for Linux
source venv/bin/activate
```

4. Install requirements:
``` bash
pip install -r requirements.txt
```

5. Initialize database:
``` bash
python3 manage.py makemigrations
python3 manage.py migrate
```

6. [OPTIONAL] Create superuser/admin:
``` bash
python3 manage.py createsuperuser
```  
   Then set your own admin account.

7. Run development server:
``` bash
python manage.py runserver
```

8. Open your sever by going to `localhost:8000/` in your browser.

## Usage
1. Log in
2. Create courses and sections
3. Add students to sections
4. Create test for courses
5. Enter student scores for each test.
