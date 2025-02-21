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

### STEP 03- Change database creadential

```bash

inventory_management\settings\development.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '', # Replace your DB name here
        'USER': '', # Replace your DB user here
        'PASSWORD': '', # Replace your DB password here
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
