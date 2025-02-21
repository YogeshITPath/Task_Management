# How to run?
### STEPS:

### Python version 3.10.0

Clone the repository

```bash
git clone https://github.com/YogeshITPath/Task_Management.git
cd Task_Management
```

### STEP 01- Create a virtual environment after opening the repository

```bash
python -m venv venv
.\venv\Scripts\activate #window
source venv\bin\activate #linux
```

### STEP 02- install the requirements

```bash
pip install -r requirements.txt
```

### STEP 03- Change database credential

```bash

task_management_system\settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'task_management_system', # Replace your DB name here
        'USER': 'postgres', # Replace your DB user here
        'PASSWORD': 'ips12345', # Replace your DB password here
        'HOST': 'localhost',
        'PORT': '5432', # Replace your DB port here
    }
}
```

### STEP 04- Create table inside database

```bash
python manage.py migrate
```

### STEP 05- Run server

```bash
python manage.py runserver
```

### Your project is runnning on this URL
```bash
http://127.0.0.1:8000/
```
