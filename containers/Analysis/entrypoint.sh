#! /bin/sh

cp delivery.json $COMED_DATA_DIRECTORY
cd $COMED_DATA_DIRECTORY

/MakeComEdDataFrame.py
/MakeEnphaseDataFrame.py
/MakeEmporiaDataFrame.py

/ComedAnalysis.py
/EnphaseAnalysis.py
/EmporiaAnalysis.py

/MonthlyCost.py

sleep 1800
