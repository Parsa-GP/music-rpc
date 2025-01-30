#!/bin/bash
args="["

for arg in "$@"; do
    args+="\"$arg\", "
done
args="${args%, }"
args+="]"
if tmux has-session -t cmus-rpc 2>/dev/null; then
    tmux send-keys -t cmus-rpc C-c
else
    tmux new-session -d -s cmus-rpc
    tmux send-keys -t cmus-rpc "cd /home/parsa/projects/python/cmus-discord/" C-m
fi
tmux send-keys -t cmus-rpc "python3 client-cmus.py '$args'" C-m

