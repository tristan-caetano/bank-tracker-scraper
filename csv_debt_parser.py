import subprocess
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os
from os.path import exists
import sqlite3
from dotenv import load_dotenv
import cit_csv_scrape_downloader as scraper

# Getting the csv file
def locate_csv(in_date):

    # Starting query input
    # Query ID, cost, month, year
    query_input = []
    query_input.append(get_profile_id(init_DB()))

    # Initiating variables
    running_credits = 0 # Gets all the current credits to my account
    running_net = 0 # Gets the current net spending for the month
    running_expenses = 0 # Gets all expenses for the month, regardless of credits

    # Getting current date
    #curr_date = datetime.now()
    curr_date = datetime.strptime(in_date, "%m/%d/%Y")
    curr_month = curr_date.month
    curr_year = curr_date.year

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
    
    print(f"Current {curr_date.strftime("%B")} {curr_date.strftime("%Y")} Net: {running_net}")
    
    query_input.append(running_net)
    query_input.append(curr_date.strftime("%B"))
    query_input.append(curr_date.strftime("%Y"))
    
    # print("Current", curr_date.strftime("%B"), "Total Expenses:", running_expenses)
    # print("Current", curr_date.strftime("%B"), "Total Credits:", running_credits)

    return query_input

# Grab spending for the previous number of months
def get_previous_months(months):

    # Running scraper and bash script to grab csv
    scraper.cit_login()
    subprocess.run(["bash", "csv_grabber.sh"])

    # Changeable number to determine how many months still need to be grabbed for expenses
    month_iterator = months

    # Total monthly net for all the months that have been given
    total_net = 0

    # Getting current month spending
    curr_date = datetime.now()
    curr_date_formatted = curr_date.strftime("%m/%d/%Y")
    month_one = locate_csv(str(curr_date_formatted))
    add_monthly_expenses(init_DB(), month_one)
    
    month_iterator -= 1

    # Changeable value for the month starting from the current month
    prev_month = curr_date

    # Going back the specified number of months
    for month in range(month_iterator):
        prev_month = prev_month - relativedelta(months=1)
        curr_month_expenses = locate_csv(str(prev_month.strftime("%m/%d/%Y")))
        total_net += curr_month_expenses[1]
        add_monthly_expenses(init_DB(), curr_month_expenses)
    
    print(f"The total net for the last {months} months is ${total_net}.")

    # Deleting the csv file
    os.remove("CiTCSV/RecentTransactions.csv")

# Initializing database
def init_DB():

    # Name of default vinyl record CSV file
    record_sql = "../finance-budgeting-app/finance.db"

    # Making sure the SQL exists
    if not exists(record_sql):
        # Connecting to DB
        con = sqlite3.connect(record_sql)
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE budgeting_profiles(ID INTEGER PRIMARY KEY, name TEXT, income REAL, payinterval TEXT)")
        cur.execute(
            "CREATE TABLE expense_profiles(ID INTEGER, name TEXT, cost REAL, payinterval TEXT)")
        cur.execute(
            "CREATE TABLE mortgage_profiles(ID INTEGER, name TEXT, cost REAL, downpayment REAL, interestrate REAL)")
        cur.execute(
            "CREATE TABLE tracking_profiles(ID INTEGER, name TEXT, cost REAL, day INTEGER, month INTEGER, year INTEGER)")
        cur.execute(
            "CREATE TABLE monthly_expenses(ID INTEGER, cost REAL, month TEXT, year TEXT, PRIMARY KEY (ID, month, year))")

    else:
        # Connecting to DB
        con = sqlite3.connect(record_sql)

    # Returning DB info
    return con

    # Query to get all profile names
def get_profile_id(con):
    
    cur = con.cursor()
    
    get_id = 0

    # Getting id from name in db
    load_dotenv()
    name = os.getenv("DB_NAME")

    # Query to get record info for 1 specific album by name
    query = 'SELECT ID FROM budgeting_profiles WHERE name IS "'+str(name)+'"'
    result = cur.execute(query)

    # Getting the profile id, there should only be one
    for id in result:
        get_id = id[0]

    # Returning DB data
    return get_id


# Adding expenses to db
def add_monthly_expenses(con, record):

    # Getting DB info
    cur = con.cursor()

    # Sending 1 entry to the DB
    cur.execute("INSERT OR REPLACE INTO monthly_expenses (ID, cost, month, year) VALUES (?, ?, ?, ?)", record)

    # Saving database info
    con.commit()

get_previous_months(6)