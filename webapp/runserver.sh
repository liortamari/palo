#!/bin/bash

gunicorn --workers 4 --name app -b 0.0.0.0:8080 palo.palo:app