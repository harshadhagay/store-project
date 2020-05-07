import cgi
from DBConnection import DBConnection
import os
import cgitb

cgitb.enable()
claim_file_path = os.path.normpath(os.getcwd() + os.sep + os.pardir ) + "\dynamic" 
    
def show_error(error_message):
    #get current directory path
    file = ''
    occurred = False
    with open(claim_file_path + "\claim.html",'r') as claim:
        for line in claim:
            if not occurred and '%s' in line:
                line = line % error_message
                occurred = True
            file += line
    print(file)
    
form = cgi.FieldStorage()
policy_id = form.getvalue('policy_id')
space = ' '

print("Content-type: text/html\n\n")

# connect to database 
dbConnection = DBConnection()
conn = dbConnection.get_connection_object()
cursor = conn.cursor()

# execute a SQL query using execute() method to insert a row
sql_str = "select * from policy where policy_id = %s" 
cursor.execute(sql_str % policy_id)
row = cursor.fetchone()
#print(row.user_name)


if row is None:
    show_error("Policy Id is Wrong. Please check your Policy Id")
else:
    user_name = row[1]
    user_mobile = row[2]
    user_email = row[3]
    user_addr = row[4]
    user_regno = row[5]
    user_car = row[6]
    user_car_engine = row[7]
    user_car_chassis = row[8]
    user_car_year = row[9]
    user_car_value = row[10]
    policy_start_dt = row[11]
    policy_end_dt = row[12]
    total_policy_gross_amt = row[14]
    third_party_amt = row[17]
    

    # view certificate for finalizing the insurance amount
    with open(claim_file_path + "\claim.html",'r') as claim:
        lines = claim.read().replace("\n","")
        print(lines.format(**locals()))

dbConnection.close_database()
