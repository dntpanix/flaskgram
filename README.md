# Flaskygram
Python Flask Instagram emulator
Current UI is 1:1 DOM copy of (c)Instagramm, but some styles doestn shows propertly - IDK why...
<img width="1475" height="881" alt="Flaskygram current view" src="https://github.com/user-attachments/assets/d0bc7336-3661-4cd8-9e6a-64084c0c0c20" />


Backend based on  https://github.com/YashMarmat/Instagram-clone-with-FLASK/

## Installation
after downloading/cloning the repository code, follow below steps:

### Backend

- create your virtual environment
`python -m venv myenv` 

- activate your virtual environment
`myenv\scripts\activate`

- install project dependencies
`pip install -r requirements.txt`

- for Windows 
```
pip install --only-binary :all: greenlet
pip install --only-binary :all: Flask-SQLAlchemy
```
- init python flask project
`python main.py`

- create your flask database
`flask db init`

- make your first migration
`flask db migrate -m "create tables"`

- upgrade or update your database
`flask db upgrade`

### Initial Setup
- running following commands in shell

    `python scripts/setup_roles.py`

    (to avoid roles related issues, by default application will provide you user role permissions), so with below command we are setting up 3 types of roles: User, Moderator and Administrator
    `python seed.py`
    (to seed some initial data into the database, this will create 3 users: themepark, blackjack and hookers with password as "password123")

### Running the Application

- finally run the application
`flask run`

* Note: if the application is not recognizing localhost then use its address instead like this => `http://127.0.0.1:5000/login`, make sure to not include extra slashes "/" at the end of your endpoint or api to avoid not found issues, please use the urls as mentioned in views.


## All set ! Happy coding :)
