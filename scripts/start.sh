#!/bin/bash

# set judge server state "running"
bash onigiri_war_judge/test_scripts/set_running.sh localhost:5000

# launch robot control node
roslaunch onigiri_war sim_robot_run.launch
