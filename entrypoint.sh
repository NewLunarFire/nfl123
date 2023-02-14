#!/bin/sh

alembic upgrade head
gunicorn app:app --bind 0.0.0.0