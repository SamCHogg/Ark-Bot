#!/bin/bash

while true; do
    python3 arkbot.py

	echo "Rebooting in:"
	for i in 10 9 8 7 6 5 4 3 2 1
	do
		echo "$i..."
		sleep 1
	done
	echo "Rebooting now!"
done
