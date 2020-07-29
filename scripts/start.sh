#!/bin/bash

# set default level 1
VALUE_L="1"


# get args level setting
while getopts l: OPT
do
  case $OPT in
    "l" ) FLG_L="TRUE" ; VALUE_L="$OPTARG" ;;
  esac
done

# set judge server state "running"
bash judge/test_scripts/set_running.sh localhost:5000

# launch robot control node
roslaunch burger_war sim_robot_run.launch enemy_level:=$VALUE_L
