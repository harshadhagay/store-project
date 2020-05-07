# make payment using ccavenue.com, the largest payment gateway in India

import cgi, webbrowser, os

form1 = cgi.FieldStorage()
user_amt = form1.getvalue('user_amt')
if user_amt is not None:
    total_amt_to_be_paid = float(user_amt)
lines = ''

print("Content-type: text/html\n\n")

# function to display payment information
def pay_amount(total_amt_to_be_paid):
    #open the file, read it and modify the amount, store it in a variable
    """with open((os.path.normpath(os.getcwd() + os.sep + os.pardir)+"/dynamic/payment_gateway.html"),'r') as payment_gateway_file:
        lines = payment_gateway_file.read()
        lines = lines.format(**locals())
    
    #write the modified lines into a new file
    with open((os.path.normpath(os.getcwd() + os.sep + os.pardir)+"/dynamic/payment_gateway1.html"),'w') as payment_gateway_file:
        payment_gateway_file.write(lines)
        
    # open the new file which is generated in a new browser page.
    webbrowser.open_new_tab(os.path.normpath(os.getcwd() + os.sep + os.pardir)+"/dynamic/payment_gateway1.html")"""
    webbrowser.open_new_tab(os.path.normpath(os.getcwd() + os.sep + os.pardir)+"/dynamic/gateway.html")

# call the above function and pass the premium amount
pay_amount(total_amt_to_be_paid)
