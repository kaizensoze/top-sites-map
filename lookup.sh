#!/usr/local/bin/zsh

rank=0
for i in `cat data.json | jq -r '.[] | .host'`
do
((rank++))
local address=$(host2address $i)
echo "| $rank | $i | $address |"
done