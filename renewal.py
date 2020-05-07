import cgi, webbrowser
import os
from DBConnection import DBConnection
from datetime import datetime
from datetime import timedelta

def show_error(error_message):
    #get current directory path
    renewal_file_path = os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + os.pardir) 
    file = ''
    occurred = False
    with open((renewal_file_path + '/renewal.html'),'r') as renewal:

        for line in renewal:
            if not occurred and '%s' in line:
                line = line % error_message
                occurred = True
            file += line
    print(file)


form = cgi.FieldStorage()
policy_id = form.getvalue('policy_no')
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

# disconnect from db
dbConnection.close_database()

if row is None:
    show_error("Policy Id not Found. Please check your policy id")
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
    user_car_year = int(user_car_year)
    user_car_value = row[10]
    user_car_value = float(user_car_value)
    policy_end_dt = row[12]
    policy_end_month = int(policy_end_dt.split(" ")[0].split("-")[1])

    #print(user_name,user_mobile,user_email,user_addr,user_regno,user_car,user_car_engine,user_car_chassis,user_car_year,user_car_value)

    # know the server date and time 
    dt = datetime.now()
    policy_start_dt = str(dt)[:-3]

    period = timedelta(days=365)  # to get date after 1 year
    dt1 = dt+period
    policy_end_dt = str(dt1)[:-3]

    # take current year from date
    current_year = dt.year
    current_month = dt.month

    # find the years elapsed 
    period = current_year - int(user_car_year)

    if period == 0 and (policy_end_month > current_month):
            with open(os.path.normpath(os.getcwd() + os.sep + os.pardir)+ "/dynamic/alertbox.html",'r') as alertbox:
                    lines = alertbox.read().replace("\n","")
                    print(lines)
    else:
        # calculate depreciation
        yearly_dep = user_car_value/15  # the life of car is 15 years
        total_amtal_dep = period * yearly_dep
        cost = user_car_value - total_amtal_dep # this is the coverage amount
        policy_amount = cost * 0.1  # this is the policy amount 
        # calculate premium details separately
        gst = policy_amount * 0.18  # gst is 18% in total amount
        policy_amount = policy_amount - gst  # reduce gst
        basic = policy_amount * 0.40  # 40% of amount goes as basic insurance
        third_party_amt = policy_amount * 0.60  # 60% goes as third party insurance
        total_amt = basic+third_party_amt
        cgst = gst/2   # central gst is 9%
        sgst = gst/2   # state gst is 9%
        total_policy_gross_amt = basic + third_party_amt + cgst + sgst   # to be payable

        #limit the precision of floating variables to 2
        policy_amount ='{:.2f}'.format(policy_amount,)
        basic = '{:.2f}'.format(basic,)
        third_party_amt = '{:.2f}'.format(third_party_amt,)
        total_amt = '{:.2f}'.format(total_amt,)
        total_policy_gross_amt = '{:.2f}'.format(total_policy_gross_amt,)

        # display the policy certificate
        # view certificate for finalizing the insurance amount
        with open(os.path.normpath(os.getcwd() + os.sep + os.pardir)+ "/dynamic/certificate.html",'r') as certificate:
            lines = certificate.read().replace("\n","")
            print(lines.format(**locals()))
