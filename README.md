# flaskgram
Python Flask Instagramm emulator

based on  https://github.com/YashMarmat/Instagram-clone-with-FLASK/

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

- run the project
`flask run`

- open a new terminal window follow below commands(keep the application running)

`flask shell`

- running following commands in shell (to avoid roles related issues, by default application will provide you user role permissions), so with below command we are setting up 3 types of roles: User, Moderator and Administrator

`Role.insert_roles()`

- confirm roles

`Role.query.all()`

- exit shell

`exit()`

- As your application is entirely new so there is no data in it so go ahead and signup and login to create your new account (i highly recommend to import the json file present in "project_files" directory to ease your work)

* Note: if the application is not recognizing localhost then use its address instead like this => `http://127.0.0.1:5000/login`, make sure to not include extra slashes "/" at the end of your endpoint or api to avoid not found issues, please use the urls as mentioned in views.


## All set ! Happy coding :)
