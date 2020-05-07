#this program gives the reports between two dates

import cgi
from datetime import datetime, date
from DBConnection import DBConnection
import os

print("Content-type: text/html\n\n")

#get form values
form = cgi.FieldStorage()
dateStart = form.getvalue('dateStart')
dateStart = datetime.strptime(dateStart, '%m/%d/%Y').date()
#formatting date to month-day-year
start = ''+ str(dateStart.year) + '-'
if len(str(dateStart.month)) == 1:
    start += '0' + str(dateStart.month) + '-'
else:
    start += str(dateStart.month) + '-'
    
if len(str(dateStart.day)) is 1:
    start += '0'+str(dateStart.day)
else:
    start += str(dateStart.day)

#simillarly do for dateend
dateEnd = form.getvalue('dateEnd')
dateEnd = datetime.strptime(dateEnd, "%m/%d/%Y").date()
end = '' + str(dateEnd.year) + '-'
if len(str(dateEnd.month)) is 1:
    end += '0'+str(dateEnd.month)+'-'
else:
    end += str(dateEnd.month)+'-'

if len(str(dateEnd.day)) is 1:
    end += '0'+str(dateEnd.day)
else:
    end += str(dateEnd.day)

dbConnection = DBConnection()
conn = dbConnection.get_connection_object()
cursor = conn.cursor()

sql = "SELECT policy_start_dt FROM policy"
#connect to database
dbConnection = DBConnection()
conn = dbConnection.get_connection_object()
cursor = conn.cursor()
cursor.execute(sql)
records = cursor.fetchall()
#print(records)
record_list = []
#get the dates of the reports in the range
if records is not None:
    for date in records:
        db_record_date = date[0].split(' ')[0]
        if start <= db_record_date or db_record_date <= end:
            record_list.append(date[0])
            # print(db_record_date)

def show_reports_in_table(record_list):
    td_class_line = ''
    td_data_line = ''
    with open(os.path.normpath(os.getcwd() + os.sep + os.pardir)+"/dynamic/table.html", 'r') as file:
        table = file.read().split('\n')
        i = 0
        while i < len(table):
            line = (table[i])
            if "<th> %s " in line:
                print(line % 'Total Gross Insurance Amount')
                i = i+1
                continue
            if "<td class='nr'>" in line:
                nr_index = i
                for date in record_list:
                    sql = "select (policy_id),(user_name),(user_email),(total_policy_gross_amt) from policy where policy_start_dt = '%s'"
                    cursor.execute(sql % (date,))
                    record = cursor.fetchone()  # gives a tuple of tuple

                    if record is not None:
                        for element in record:
                            # below if cond sets only nr class statement in table.html
                            if td_class_line == '' or td_class_line == '<tr>':
                                td_class_line += line % element
                                print(td_class_line)
                                i = nr_index + 1
                                line = table[i]
                            else:
                                td_data_line += line % element

                    # td_data_line += "<td> <button type='button' id = 'btn' >Send Mail</button> </td>"
                    td_data_line += '</tr>'
                    print(td_data_line)
                    td_data_line = ''

                    td_class_line = '<tr>'
                    i = nr_index
                    line = table[i]
                i = nr_index + 3
            else:
                print(line)
                i = i + 1


show_reports_in_table(record_list)
dbConnection.close_database()