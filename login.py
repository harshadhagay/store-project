import cgi, pymysql
import inspect, os
from DBConnection import DBConnection

print("Content-type: text/html\n\n")

def show_error(error_message):
    #get current directory path
    login_file_path = os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + os.pardir + os.sep + os.pardir) 
    file = ''
    occurred = False
    with open(login_file_path + "\login.html",'r') as login:
        for line in login:
            if not occurred and '%s' in line:
                line = line % error_message
                occurred = True
            file += line
    print(file)

def show_after_login_page():
    with open(os.path.normpath(os.getcwd() + os.sep + os.pardir)+'/dynamic/afterLogin.html') as afterLogin:
        print(afterLogin.read())
		
#get form values
form = cgi.FieldStorage()
#connect to database
dbConnection = DBConnection()
conn = dbConnection.get_connection_object()
cursor = conn.cursor()

#get username from login form
username = form.getvalue('username')
#print(username)
#check if the user name is present in the database

sql = "select * from admin_login where admin_user_email = '%s'"
#print(sql % username)
cursor.execute(sql % username)

row = cursor.fetchone()
if row is not None and row[1] == username:
    password = form.getvalue('password')
    if password is not None and password == row[2]:
        show_after_login_page()
    else:
        show_error("Password is incorrect")    
else:
    show_error("Username Not Found")