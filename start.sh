#!/bin/zsh
clear
echo "Removing logs dir"
rm -rf logs
echo "Removing assets"
rm -rf assets
source .venv/bin/activate
echo "Starting scirpt"
python monitor.py -d 
