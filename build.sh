#!/usr/bin/env bash
pip install -r requirements.txt
python app.py collectstatic --noinput
python app.py migrate
