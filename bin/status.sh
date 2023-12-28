#!/bin/bash

# show status of gubnicorn and nginix

echo "
**** system status of nginx and gunicorn ****
"
sudo systemctl status nginx > status.txt
sudo systemctl status gunicorn.service >> status.txt
cat status.txt
echo "
**********"
