#! /bin/bash

podman build . -f containers/Enphase/Containerfile -t ericvaandering/solar-monitoring:1.0.0
podman push ericvaandering/solar-monitoring:1.0.0
