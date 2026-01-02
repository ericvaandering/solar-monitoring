#! /bin/bash

#cd ~/solar-monitoring/
podman build . -f containers/Enphase/Containerfile -t ericvaandering/solar-monitoring:0.2.0
podman push ericvaandering/solar-monitoring:0.2.0
