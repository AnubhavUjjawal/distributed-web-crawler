#!/bin/bash
kill $(lsof -t -i:8000)
kill $(lsof -t -i:8001)
kill $(lsof -t -i:8002)
