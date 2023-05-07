import pypyodbc as odbc

username = 'azureuser'
password = 'userAzure!'
server = 'hash-url.database.windows.net'
database = 'hash-urls-database'
connection_string = 'DRIVER={ODBC Driver 18 for SQL server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password

conn = odbc.connect(connection_string)
cursor = conn.cursor()
cursor.execute(''' DROP TABLE IF EXISTS urls;''')
conn.commit()
