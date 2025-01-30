#!/bin/bash

args="["

for arg in "$@"; do
    args+="\"$arg\", "
done
args="${args%, }"
args+="]"
tmux new-session -d -s cmus-rpc
tmux send-keys -t cmus-rpc C-c
tmux send-keys -t cmus-rpc "cd /home/parsa/projects/python/cmus-discord/" C-m
tmux send-keys -t cmus-rpc "python3 cmus-rpc.py '$args'" C-m

