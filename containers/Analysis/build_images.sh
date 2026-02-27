#! /bin/bash

#cd ~/solar-monitoring/
podman build . -f containers/Analysis/Containerfile -t ericvaandering/solar-analysis:0.2.0
podman push ericvaandering/solar-analysis:0.2.0
