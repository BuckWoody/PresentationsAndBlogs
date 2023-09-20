# Set up the libraries for the configuration and base web interfaces
import os
import json
from flask import Flask
from flask_restful import Resource, Api
from dotenv import load_dotenv
import pyodbc

# Load the variables from the .env file
load_dotenv()

# Create the Flask-RESTful Application
app = Flask(__name__)
api = Api(app)

# Create connection to Azure SQL DB using the config.ini file values
server_name = os.getenv('SQL_SERVER_ENDPOINT')
database_name = os.getenv('SQL_SERVER_DATABASE')
user_name = os.getenv('SQL_SERVER_USERNAME')
password = os.getenv('SQL_SERVER_PASSWORD')

# Connect to Azure SQL DB using the pyodbc package
# Note: You may need to install the ODBC driver if it is not already there. You can find that at:
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#version-17
connection = pyodbc.connect(f'Driver=ODBC Driver 17 for SQL Server;Server={server_name};Database={database_name};uid={user_name};pwd={password}')

# Create the SQL query to run against the database
def query_db():
    cursor = connection.cursor()
    # Cast is needed to corretly inform pyodbc of output type is NVARCHAR(MAX)
    # Needed if generated json is bigger then 4000 bytes and thus pyodbc trucates it
    # https://stackoverflow.com/questions/49469301/pyodbc-truncates-the-response-of-a-sql-server-for-json-query
    cursor.execute("SELECT CAST(( SELECT [ProductID], [Name], [Description] FROM [SalesLT].[vProductAndDescription] WHERE Culture = 'EN' FOR JSON AUTO ) AS NVARCHAR(MAX)) AS JsonResult;")
    result = cursor.fetchone()
    cursor.close()
    return result

# Create the class that will be used to return the data from the API
class Products(Resource):
    def get(self):
        result = query_db()
        json_result = {} if (result == None) else json.loads(result[0])     
        return json_result, 200

# Set the API endpoint to the Products class
api.add_resource(Products, '/products')

# Start App on default Flask port 5000
if __name__ == "__main__":
    app.run(debug=True)