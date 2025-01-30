#!/bin/bash
echo -n "[" > /tmp/cmus_status.json

for arg in "$@"; do
    echo -n "\"$arg\", " >> /tmp/cmus_status.json
done
sed -i 's/, *$//g' /tmp/cmus_status.json

echo "]" >> /tmp/cmus_status.json

python3 /home/parsa/projects/python/cmus-discord/cmus-rpc.py 
