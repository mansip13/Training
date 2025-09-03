#!/bin/sh 

echo "================System Information================" 
echo "Hostname: $(hostname)"
echo "Date and Time:  $(date)"
echo "Uptime: $(uptime -p)"
echo "Logged in Users: $(who | wc -l)" 

# 
echo "===============Resource  Usage================" 
echo "cpu: load: $(uptime | awk -F 'load average: ' '{print $2}')"
echo " Memory Usage: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "Disk Usage: $(df -h / | awk 'NR==2{print $3 "/" $2}')"

