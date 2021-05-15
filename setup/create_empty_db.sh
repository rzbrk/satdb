#!/bin/bash

# Check if we are root. If not, exit
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
