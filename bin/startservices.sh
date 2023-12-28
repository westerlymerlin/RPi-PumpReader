#!/bin/bash

# start services

echo "starting nginx"
sudo systemctl start nginx

echo "starting gunicorn and python app"
sudo systemctl start gunicorn.service

echo "services started"
