#!/bin/bash

imageName=wxapp
tag=1.0

dockerPort=8000
hostPort=8080

dockerLogPath=/home
hostLogPath=/home/ouyc/java/wxapp/logs

dockerTimeZoneFile=/etc/timezone
hostTimeZoneFile=/home/ouyc/java/wxapp/timezone

dockerLocalTime=/etc/localtime

hostLocalTime=/etc/localtime

docker builder prune
docker build -t ${imageName}:${tag} .
docker run -d -p ${hostPort}:${dockerPort} -v ${hostLogPath}:${dockerLogPath}  -v ${hostTimeZoneFile}:${dockerTimeZoneFile} -v ${hostLocalTime}:${dockerLocalTime}  ${imageName}:${tag}

echo "============================================================================"
docker images | grep REPOSITORY
docker images | grep ${imageName}|grep ${tag}

echo "============================================================================"
docker container list  | grep CONTAINER
docker container list |grep ${imageName} |grep ${tag}

echo "查看日志、登录容器的指令如下："
echo "docker logs -tf --tail=100 $(docker container list |grep ${imageName} |grep ${tag} | awk '{print $1}') "
echo "docker exec -it  $(docker container list |grep ${imageName} |grep ${tag} | awk '{print $1}') /bin/sh"

echo "start finish"