#!/bin/bash

list=`docker images |awk '{print $1,$2}'`
echo "============================================================================"
imageName=wxapp
tags=1.0
echo "remove $imageName:$tags "
echo "============================================================================"

docker stop  $(docker ps -a |grep $imageName | grep $tags | awk '{print $1}' )
docker rm  $(docker ps -a |grep $imageName| grep $tags | awk '{print $1}')

docker container list
echo "container cleaned.."
echo "============================================================================"
docker rmi  $(docker images |grep $imageName| grep $tags | awk '{print $3}')

docker images
echo "image cleaned.."
echo "============================================================================"
echo "remove job finished"