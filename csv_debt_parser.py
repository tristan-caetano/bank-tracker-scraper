import subprocess

# Getting the csv file
def locate_csv():

    # Running bash script to grab csv
    subprocess.run(["bash", "csv_grabber.sh"])

    # Grabbing CSV file
    csv_filename = "RecentTransactions.csv"
    cit_csv = pd.read_csv(csv_filename, low_memory=False, encoding)