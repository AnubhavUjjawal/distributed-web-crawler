#!bin/bash
source ../crawler-env/bin/activate
rpyc_classic.py --port 8000 &
rpyc_classic.py --port 8001 &
rpyc_classic.py --port 8002