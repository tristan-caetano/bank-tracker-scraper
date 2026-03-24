#! /bin/bash

# Getting the current directory, making a folder to put the transaction csv in, and fetching the csv from the downloads folder
CURR_DIR=$(pwd)
mkdir -p $CURR_DIR/CiTCSV
mv /home/$USER/Downloads/Transactions*.csv $CURR_DIR/CiTCSV/RecentTransactions.csv