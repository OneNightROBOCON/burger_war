#!/bin/bash

# 1. set state running

############# How to use #########################
# Args {server IP(default localhost:5000)}

# {server IP} localhost:5000

########## setting #########################

SERVER_IP=$1

########### script ########################
# set state to "running"
echo "=================set state "running"======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"state":"running"}' ${SERVER_IP}/warState/state

