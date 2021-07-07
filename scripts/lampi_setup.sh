#! /usr/bin/bash
echo "Installing PySimpleGUI"
pip3 install pysimplegui

echo installing RClone
curl https://rclone.org/install.sh | sudo bash

echo "Creating output folders"
mkdir /home/pi/LamPi/sync
mkdir /home/pi/LamPi/sync/videos
mkdir /home/pi/LamPi/sync/timelapse
mkdir /home/pi/LamPi/sync/logs

echo "Copying launcher to Desktop"
cp /home/pi/LamPi/launcher/lampi_start.desktop /home/pi/desktop

echo "Starting RClone to configure OneDrive sync"
echo "Choose option 26 for OneDrive, then accept all defaults"
rclone config

echo "Scheduling restart on boot"
restartcmd="python3 /home/pi/LamPi/scripts/lampi_run_terminal.py 2>&1" 
restartjob = "@reboot $croncmd"
rclonecmd="rclone copy /home/pi/Lampy/sync/ Lampi_sync: 2>&1" 
rclonejob = "*/5 * * * * $rclonecmd"

( crontab -l | grep -v -F "$restartcmd" ; echo "$restartjob" ) | crontab -
( crontab -l | grep -v -F "$rclonecmd" ; echo "$rclonejob" ) | crontab -
