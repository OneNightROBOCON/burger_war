#!/bin/bash
set -e
set -x

# judge
# run judge server and visualize window
gnome-terminal -e "python onigiri_war_judge/judgeServer.py"
gnome-terminal -e "python onigiri_war_judge/visualizeWindow.py"

# init judge server for sim setting
bash onigiri_war_judge/test_scripts/init_single_play.sh onigiri_war_judge/marker_set/sim.csv localhost:5000 foo bar

# robot
roslaunch onigiri_war turtlebot_setup_sim.launch

