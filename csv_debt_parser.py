import subprocess
from datetime import datetime
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

    for index, row in cit_csv.iterrows():
        datetime_trans = datetime.strptime(row['Date'], "%m/%d/%Y")
        if datetime_trans.month == curr_month and datetime_trans.year == curr_year:
            if row['Transaction Type'] == "CREDIT":
                running_net += float((row['Credits(+)']).replace("$", ""))
                running_credits += float((row['Credits(+)']).replace("$", ""))
                print("Credit:", float((row['Credits(+)']).replace("$", "")))

            else: 
                running_net += float((row['Debits(-)']).replace("$", "")) 
                running_expenses += float((row['Debits(-)']).replace("$", ""))
                print("Debit:", float((row['Debits(-)']).replace("$", "")))
    
    print("Current", curr_date.strftime("%B"), "Net:", running_net)
    print("Current", curr_date.strftime("%B"), "Total Expenses:", running_expenses)
    print("Current", curr_date.strftime("%B"), "Total Credits:", running_credits)

    return running_net

            
locate_csv("11/25/2025")