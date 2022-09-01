#!/bin/bash

source /home/pashbyl/projects/Fictionary/.venv/bin/activate && /home/pashbyl/projects/Fictionary/.venv/bin/gunicorn --workers 1 --bind 0.0.0.0:8000 --capture-output --log-level debug wsgi:app
