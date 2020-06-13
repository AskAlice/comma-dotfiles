#!/bin/bash
SYSTEM_BASHRC_PATH=/home/.bashrc
COMMUNITY_PATH=/data/community
COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma

git -C ${OH_MY_COMMA_PATH} pull
sh ${OH_MY_COMMA_PATH}/install.sh 'update'