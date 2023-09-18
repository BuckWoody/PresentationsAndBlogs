import configparser
from flask import Flask
import pyodbc

app = Flask(__name__)

# creating connection Object which will contain SQL Server Connection
config = configparser.ConfigParser()
config.read('config.ini')
ServerName = config.get('Connection', 'SQL_SERVER_ENDPOINT')
DatabaseName = config.get('Connection', 'SQL_SERVER_DATABASE')
UserName = config.get('Connection', 'SQL_SERVER_USERNAME')
PasswordValue = config.get('Connection', 'SQL_SERVER_PASSWORD')

connection = pyodbc.connect(f'Driver=ODBC Driver 17 for SQL Server;Server={ServerName};Database={DatabaseName};uid={UserName};pwd={PasswordValue}')
cursor = connection.cursor()
cursor.execute("SELECT FullName, SalesTerritory FROM [Sales].[vSalesPersonSalesByFiscalYears];")

strContent= "<table style='border:1px solid red'>"
for row in cursor:
    strContent= strContent+ "<tr>"
    for dbItem in row:
        strContent= strContent+ "<td>" + str(dbItem) + "</td>"
    strContent= strContent+ "</tr>"
strContent= strContent+ "</table>"
connection.close()

@app.route('/')
@app.route('/home')
def home():
    return "<html><body>" + strContent + "</body></html>"

if __name__ == "__main__":
    app.run(debug=True)