#!/usr/local/bin/zsh

rank=0
for i in `cat hosts.txt`
do
((rank++))
local address=$(host2address $i)
echo "| $rank | $i | $address |"
done