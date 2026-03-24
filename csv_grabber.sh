#! /bin/bash

CURR_DIR=$(pwd)

mkdir -p $CURR_DIR/CiTCSV

mv /home/$USER/Downloads/Transactions*.csv $CURR_DIR/CiTCSV/RecentTransactions.csv