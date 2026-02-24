#! /bin/sh

cp delivery.json $COMED_DATA_DIRECTORY
cd $COMED_DATA_DIRECTORY

/MakeComEdDataFrame.py

/MonthlyCost.py

sleep 3600
