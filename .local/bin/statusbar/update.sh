#!/bin/bash


updates=$(apt-get -q -y --ignore-hold --allow-change-held-packages --allow-unauthenticated -s dist-upgrade | /bin/grep  ^Inst | wc -l)

if [ $updates -gt 0 ]; then
	printf " $updates"
else
	echo ""
fi
