import subprocess
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

# Getting the csv file
def locate_csv(in_date):

    # Initiating variables
    running_credits = 0 # Gets all the current credits to my account
    running_net = 0 # Gets the current net spending for the month
    running_expenses = 0 # Gets all expenses for the month, regardless of credits

    # Getting current date
    #curr_date = datetime.now()
    curr_date = datetime.strptime(in_date, "%m/%d/%Y")
    curr_month = curr_date.month
    curr_year = curr_date.year

    # Running bash script to grab csv
    # subprocess.run(["bash", "csv_grabber.sh"])

    # Grabbing CSV file
    csv_filename = "CiTCSV/RecentTransactions.csv"
    cit_csv = pd.read_csv(csv_filename)

    # Iterating through the csv
    for index, row in cit_csv.iterrows():
        datetime_trans = datetime.strptime(row['Date'], "%m/%d/%Y")
        if datetime_trans.month == curr_month and datetime_trans.year == curr_year:
            if row['Transaction Type'] == "CREDIT":
                running_net += float((row['Credits(+)']).replace("$", ""))
                running_credits += float((row['Credits(+)']).replace("$", ""))
                #print("Credit:", float((row['Credits(+)']).replace("$", "")))

            else: 
                running_net += float((row['Debits(-)']).replace("$", "")) 
                running_expenses += float((row['Debits(-)']).replace("$", ""))
                #print("Debit:", float((row['Debits(-)']).replace("$", "")))
    
    print("Current", curr_date.strftime("%B"), "Net:", running_net)
    # print("Current", curr_date.strftime("%B"), "Total Expenses:", running_expenses)
    # print("Current", curr_date.strftime("%B"), "Total Credits:", running_credits)

    return running_net

# Grab spending for the previous number of months
def get_previous_months(months):

    # Changeable number to determine how many months still need to be grabbed for expenses
    month_iterator = months

    # Total monthly net for all the months that have been given
    total_net = 0

    # Getting current month spending
    curr_date = datetime.now()
    curr_date_formatted = curr_date.strftime("%m/%d/%Y")
    locate_csv(str(curr_date_formatted))
    month_iterator -= 1

    # Changeable value for the month starting from the current month
    prev_month = curr_date

    # Going back the specified number of months
    for month in range(month_iterator):
        prev_month = prev_month - relativedelta(months=1)
        total_net += locate_csv(str(prev_month.strftime("%m/%d/%Y")))
    
    print(f"The total net for the last {months} months is ${total_net}.")

get_previous_months(10)