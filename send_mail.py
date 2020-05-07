import cgi, pymysql, os
from DBConnection import DBConnection
print("Content-type: text/html\n\n")

def show_after_login():
    sql = "select (policy_id),(user_name),(user_email) from policy where policy_status_paid = %s"
    var = 0
    cursor.execute(sql % var)
    records = cursor.fetchall()  # gives a tuple of tuple
    td_class_line = ''
    td_data_line = ''
    with open(os.path.normpath(os.getcwd() + os.sep + os.pardir)+"/dynamic/table.html", 'r') as file:
        table = file.read().split('\n')
        i = 0
        while i < len(table):
            line = (table[i])
            if "<th> %s" in line:
                print(line % 'Send Insurance To Email')
                i = i+1
                continue
            
            if "<td class='nr'>" in line:
                nr_index = i
                for record in records:
                    for element in record:
                        #below if cond sets only nr class statement in table.html
                        if td_class_line == '' or td_class_line == '<tr>':
                            td_class_line += line % element
                            print(td_class_line)
                            i = nr_index + 1
                            line = table[i]
                        else:
                            td_data_line += line % element

                    td_data_line += "<td> <button type='button' id = 'btn' >Send Mail</button> </td>"
                    td_data_line += '</tr>'
                    print(td_data_line)
                    td_data_line = ''

                    td_class_line = '<tr>'
                    i = nr_index
                    line = table[i]
                i = nr_index + 3
            else:
                print(line)
                i = i+1


#connect to database
dbConnection = DBConnection()
conn = dbConnection.get_connection_object()
cursor = conn.cursor()
show_after_login()
#close the database
dbConnection.close_database()
