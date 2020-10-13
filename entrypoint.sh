#!/bin/sh

FLASK_ENV=development uvicorn main:app --host 0.0.0.0 --port 8000 --reload
