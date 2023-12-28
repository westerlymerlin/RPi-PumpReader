#!/bin/bash

# stop serices

echo "
**** stopping gunicoren and python app ****
"
sudo systemctl stop gunicorn.service

echo "
**** stopping nginx ****
"
sudo systemctl stop nginx

echo "
******** services stopped ********
"
