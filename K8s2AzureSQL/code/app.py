# Set up the libraries for the configuration and base web interfaces
import configparser
from flask import Flask
import pyodbc

# Open the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Create the Flask Application
app = Flask(__name__)

# Create connection to Azure SQL DB using the config.ini file values
ServerName = config.get('Connection', 'SQL_SERVER_ENDPOINT')
DatabaseName = config.get('Connection', 'SQL_SERVER_DATABASE')
UserName = config.get('Connection', 'SQL_SERVER_USERNAME')
PasswordValue = config.get('Connection', 'SQL_SERVER_PASSWORD')

# Connect to Azure SQL DB using the pyodbc package
# Note: You may need to install the ODBC driver if it is not already there. You can find that at:
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#version-17
connection = pyodbc.connect(f'Driver=ODBC Driver 17 for SQL Server;Server={ServerName};Database={DatabaseName};uid={UserName};pwd={PasswordValue}')

# Create the query and set the cursor object to hold the results
cursor = connection.cursor()
cursor.execute("SELECT [ProductID], [Name], [Description] FROM [SalesLT].[vProductAndDescription] ORDER BY [Name];")

# Display the results
strContent= "<table style='border:1px solid red'>"
for row in cursor:
    strContent= strContent+ "<tr>"
    for dbItem in row:
        strContent= strContent+ "<td>" + str(dbItem) + "</td>"
    strContent= strContent+ "</tr>"
strContent= strContent+ "</table>"
connection.close()

# Set the Flask application to run on the standard ports - typically port 5000
@app.route('/')
@app.route('/home')
def home():
    return "<html><body>" + strContent + "</body></html>"

if __name__ == "__main__":
    app.run(debug=True)