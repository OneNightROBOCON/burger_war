#!/bin/bash

# initialize game state
############# How to use #########################
# Args {makerset file} {server IP(default localhost:5000)} {red side player name} {blue side player name} 

# {marker set file}
# {red side player name} ishiro
# {blue side player name} jiro
# {server IP} localhost:5000

########## setting #########################

MARKER_SET_FILE=$1
SERVER_IP=$2
RED_PLAYER_NAME=$3
BLUE_PLAYER_NAME=$4

########### script ########################

# reset
echo "=================RESET======================"
curl ${SERVER_IP}/reset

# GET war state initial
echo "=================STATE initial======================"
curl ${SERVER_IP}/warState

# regist targets 
echo "=================REGIST targets======================"
# read marker set csv
for line in `cat ${MARKER_SET_FILE}`
do
  NAME=`echo ${line} | cut -d ',' -f 1`
  POINT=`echo ${line} | cut -d ',' -f 2`
  ID=`echo ${line} | cut -d ',' -f 3`
  # print
  echo ${NAME}
  echo ${POINT}
  echo ${ID}
  echo "{\"name\":${NAME}, \"id\":${ID}, \"point\":${POINT}}"
  # post target
  curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d "{\"name\":\"${NAME}\", \"id\":\"${ID}\", \"point\":\"${POINT}\"}" ${SERVER_IP}/warState/targets
  #curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d ${JSON} ${SERVER_IP}/warState/targets
  echo
done

# regist players
echo "=================REGIST players======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d "{\"name\":\"${RED_PLAYER_NAME}\"}" ${SERVER_IP}/warState/players
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d "{\"name\":\"${BLUE_PLAYER_NAME}\"}" ${SERVER_IP}/warState/players

