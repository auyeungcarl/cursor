#!/bin/bash
mvn clean install

cd backend/
sh ./stop.sh
sh ./start.sh

cd ..