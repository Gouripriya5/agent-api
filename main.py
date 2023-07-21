from flask import Flask
from flask_restful import Api, Resource
import oracledb
import os
# load envinornment variables from .env file
from dotenv import load_dotenv


load_dotenv()


# create the app
app = Flask(__name__)
api = Api(app)


# Access environment variablesfor Oracle Database Connectivity
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SERVICE_NAME = os.getenv("DB_SERVICE_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


@app.route("/users")
def get_users():
    users = []
    print(f'host: {DB_HOST}', f'serv: {DB_SERVICE_NAME}',
          f'user: {DB_USER}', f'pass: {DB_PASSWORD}')
    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, service_name=DB_SERVICE_NAME) as connection:
        with connection.cursor() as cursor:
            # sql = """select sysdate from dual"""
            sql = """SELECT * FROM  AGENt.Agent_users"""
            for r in cursor.execute(sql):
                users.append(
                    {'profile': {'email': r[0], 'role': r[1], 'status': r[2]}})
    return {'users': users}


@app.route("/users/<string:user_name>")
def get_user(user_name):
    user = 'no user found!'
    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, service_name=DB_SERVICE_NAME) as connection:
        with connection.cursor() as cursor:
            # sql = """select sysdate from dual"""
            sql = """SELECT * FROM  AGENt.Agent_users"""
            for r in cursor.execute(sql):
                if r[0] == user_name:
                    user = {'email': r[0], 'role': r[1], 'status': r[2]}
    return user

if __name__ == "__main__":
    app.run(debug=True)
