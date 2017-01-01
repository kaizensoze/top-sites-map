#!/usr/local/bin/zsh

# used to produce table markdown
rank=0
for i in `cat data.json | jq -r '.[] | .host'`
do
((rank++))
local address=$(host2address $i) # see zsh_functions.txt
echo "| $rank | $i | $address |"
done

