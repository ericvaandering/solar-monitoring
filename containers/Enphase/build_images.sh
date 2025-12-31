#! /bin/bash

#cd ~/solar-monitoring/
podman build . -f containers/Enphase/Containerfile -t ericvaandering/solar-monitoring:0.0.2
podman push ericvaandering/solar-monitoring:0.1.0
