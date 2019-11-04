#!/usr/bin/env bash

HEIGHT=$1

docker-compose exec mininet mn --custom /tmp/topology/fat_tree.py --topo fat_tree,${HEIGHT} --mac --arp --switch ovsk --controller remote
