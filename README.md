# SnoopJake TEAM CHANGELOG

## SonarCloud code quality fixes

### Maintability Issues

1. On **backend/emailClient/settings.py**
    > **Remove commented out code.** (Sections of code should not be commented out python:S125)
    -    >Commented-out code distracts the focus from the actual executed code. It creates a noise that increases maintenance code. And because it is never executed, it quickly becomes out of date and invalid. Change date: ***18/03/2024***
2. On **backend/emailClient/urls.py**
    > **Remove commented out code.** (Sections of code should not be commented out python:S125)
    -    >Commented-out code distracts the focus from the actual executed code. It creates a noise that increases maintenance code. And because it is never executed, it quickly becomes out of date and invalid. Change date: ***18/03/2024***
3. On **backend/email_api/tests.py**
    > **Rename this local variable "testUser"**
    -    >Local variable and function parameter names should comply with a naming convention python:S117. Change date: ***18/03/2024***
4. On **backend/.../views/email_views.py** (String literals should not be duplicated python:S1192)
    > **Define a constant instead of duplicating this literal "Email does not exist" 4 times.**
    -    >A constant was used to replace the duplicate literal strings. Change date: ***18/03/2024***
5. On **backend/email_api/tests.py** (Unused local variables should be removed python:S1481)
    > **Remove the unused local variable**
    -    >False Positive. Change date: ***18/03/2024***

### Intensionality Issues
1. On **backend/emailClient/settings.py**
    > **Remove extra validation for de Debug .env.** 
    -    >Extra validation for the Debug .env is unnecessary and may lead to confusion or inefficiency in the codebase. Removing this validation simplifies the code and ensures that configuration settings are handled consistently. This change promotes clarity and maintainability within the codebase. Change date: ***23/03/2024***


## New features

### Feature 1: Sphinx
- **Automatic Documentation with Sphinx**
  - Added automatic documentation using Sphinx to facilitate project understanding and usage.
  - **Why it's important:** Automated documentation streamlines the process of maintaining project documentation, ensuring consistency and accuracy across the codebase. It also facilitates a better understanding of the project's functionality and usage.

![image](https://github.com/Tech-Fellows-SnoopJake/hg0-emailClient-backend/assets/49454068/d2d49cd1-1ce5-419e-a2f4-5aec8ab7ca6f)


### Feature 2 :  Automated Static code review and test coverage with SonarCloud
We implemented a CI workflow that checked the code on Push and Pull Request actions on GitHub.

The overall analysis can be found at [https://sonarcloud.io/summary/overall?id=Tech-Fellows-SnoopJake_hg0-emailClient-frontend](https://sonarcloud.io/summary/overall?id=Tech-Fellows-SnoopJake_hg0-emailClient-backend)

On each commit, a SonarCloud badge can be seen, which analyzes the code and shows code quality problems:

![image](https://github.com/Tech-Fellows-SnoopJake/hg0-emailClient-backend/assets/49454068/0779fa88-4e27-44e1-b105-27d06c21c376)


We **succesfully fixed all the vulnerabilities found initially**, **for the 1.8 lines of code analyzed!**

![image](https://github.com/Tech-Fellows-SnoopJake/hg0-emailClient-frontend/assets/49454068/4285bcb7-7924-42e4-ab54-bd042e428cf9)
![image](https://github.com/Tech-Fellows-SnoopJake/hg0-emailClient-backend/assets/49454068/89b69fb0-989c-40bb-8434-3f8733e00fe0)


Test coverage was implemented, but not enough to pass the quality threshold of 80% of tests!

For the overall code, only 41.36% of test coverage was achieved, while for that specific commit, only 26.8% of the new code was tested!

![image](https://github.com/Tech-Fellows-SnoopJake/hg0-emailClient-backend/assets/49454068/25f2fe6e-9232-4e51-b154-eeb4f21e73a1)
![image](https://github.com/Tech-Fellows-SnoopJake/hg0-emailClient-backend/assets/49454068/b4dc73c7-fdf3-4be3-882e-12c4b3c75b53)




///////////////////////////////////////////////////


## Architectural Change

### Database Migration to AWS RDS MySQL

**What changed:** 
Transitioned the backend database of AwesomeMail from PostgreSQL to AWS RDS MySQL.

**Why we changed it:** 
AWS RDS MySQL offers managed MySQL database services with scalability, reliability, and security features. This allows us to focus more on application development rather than database management tasks.

**How we changed it:** 
1. Provisioned an AWS RDS MySQL instance through the AWS Management Console.
2. Configured AwesomeMail to use the AWS RDS MySQL instance as the backend database in Django settings (`settings.py`).

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'awesome_mail_db',          
        'USER': 'your_mysql_username',         
        'PASSWORD': 'your_mysql_password',     
        'HOST': 'your_rds_mysql_endpoint',                   
        'PORT': '3306',                        
    }
}
```

**Migration Steps:**

1. Opened a terminal or command prompt.
2. Navigated to the root directory of the AwesomeMail Django project.
3. Ran the following command to generate migrations:

    ```bash
    python manage.py makemigrations
    ```

    This command generated migration files based on changes to AwesomeMail's models.

4. After generating the migrations, applied them by running the following command:

    ```bash
    python manage.py migrate
    ```

    This applied pending migrations and updated the database structure to reflect changes in the models.

By migrating to AWS RDS MySQL, AwesomeMail now benefits from a managed database service, including automated backups, high availability, and scalability, while reducing operational overhead.


# Email Client Project

## Features
- Send emails through a web interface.
- Manage and store emails in PostgreSQL.
- RESTful API for interacting with the email system.
- User authentication and authorization.

## Technologies Used
- Django
- Django Rest Framework
- PostgreSQL

## Requirements
- Python 3.11 or higher
- Django 5 or higher
- Django Rest Framework
- PostgreSQL

## Environment Setup
1. Clone the repository:
    ```bash
    git clone git@github.com:zeldacamila/hg0-emailClient-backend.git
    cd backend
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Environment Variables
To run this project, you will need to add the following environment variables to your `.env` file in the project root directory. Do not include sensitive information directly in your project files or documentation.
```
SECRET_KEY='your_secret_key_here'
DEBUG='True' # Set to 'False' in production
DB_NAME='your_postgres_db_name'
DB_USER='your_postgres_user'
DB_PASSWORD='your_postgres_password'
DB_HOST='your_postgres_host'
DB_PORT='your_postgres_port'
ALLOWED_HOSTS='your_domain.com,www.your_domain.com'
```

## Usage
Access [http://localhost:8000/](http://localhost:8000/) in your browser to interact with the application.


