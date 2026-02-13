#! /bin/sh

cp delivery.json $COMED_DATA_DIRECTORY
cd $COMED_DATA_DIRECTORY
/MonthlyCost.py

sleep 3600
