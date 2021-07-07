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
,kdir /home/pi/.config/autostart

echo "Copying launcher to Desktop"
cp /home/pi/LamPi/launcher/lampi_start.desktop /home/pi/Desktop

echo "Setting up autostart"
cp /home/pi/LamPi/launcher/autostart_launcher.desktop /home/pi/.config/autostart

echo "Starting RClone to configure OneDrive sync"
rclone config

echo "Scheduling rclone scheduled backup"
rclonecmd="rclone copy /home/pi/Lampy/sync/ OneDrive:LamPi 2>&1" 
rclonejob="*/5 * * * * $rclonecmd"
( crontab -l | grep -v -F "$rclonecmd" ; echo "$rclonejob" ) | crontab -
