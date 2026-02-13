#! /bin/bash

#cd ~/solar-monitoring/
podman build . -f containers/Emporia/Containerfile -t ericvaandering/emporia-fetch:0.1.0
podman push ericvaandering/emporia-fetch:0.1.0
