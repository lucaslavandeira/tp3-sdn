#!/usr/bin/env bash
docker-compose exec mininet mn --custom /tmp/topology/line.py --topo line --mac --arp --switch ovsk --controller remote
