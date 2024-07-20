#!/bin/zsh
clear
echo "Removing logs dir"
rm -rf logs
source .venv/bin/activate
echo "Starting scirpt"
python monitor.py -d 
