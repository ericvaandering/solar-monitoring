#! /bin/bash

#cd ~/solar-monitoring/
podman build . -f containers/Analysis/Containerfile -t ericvaandering/solar-analysis:0.3.0
podman push ericvaandering/solar-analysis:0.3.0
