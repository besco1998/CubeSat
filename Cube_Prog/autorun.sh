#!/usr/bin/env bash
python camera_cubesat.py &
python gnd_requests_cubesat.py &
python telemetry_cubesat.py &
