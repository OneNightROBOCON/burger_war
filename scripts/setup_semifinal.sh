#!/bin/bash
set -e
set -x

RED_NAME=$1
BLUE_NAME=$2

# judge
# run judge server and visualize window
gnome-terminal -e "python judge/judgeServer.py --mt 180 --et 60"
gnome-terminal -e "python judge/visualizeWindow.py"

# init judge server for sim setting
bash judge/test_scripts/init_single_play.sh judge/marker_set/sim.csv localhost:5000 $RED_NAME $BLUE_NAME

# robot
roslaunch burger_war setup_sim.launch

