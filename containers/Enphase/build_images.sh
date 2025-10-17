#! /bin/bash

cd ~/solar-monitoring/
docker build . -f containers/Enphase/Containerfile -t ericvaandering/solar-monitoring:0.0.1
docker push ericvaandering/solar-monitoring:0.0.1
