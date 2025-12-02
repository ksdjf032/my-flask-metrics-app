#!/usr/bin/env bash
# build and run locally (single command)
docker build -t tiny-flask-metrics:latest .
docker run --rm -p 8080:8080 --env-file .env.example tiny-flask-metrics:latest
