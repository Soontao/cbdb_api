#!/bin/bash

cd ~/repos/cbdb_api
git pull
docker-compose down --rmi local
docker-compose up -d

exit 0