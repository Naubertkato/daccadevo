#!/bin/bash

configFile=${1:-"configs/test.yaml"}
nbRuns=${2:-1}
imageName=${3:-"daccadevo"}

memoryLimit=48G
currentPath=$(pwd)
destpath=/home/user/daccadevo
finalresultsPath=$(pwd)/results
finalresultsPathInContainer=/home/user/daccadevo/results
uid=$(id -u)

confPath=$(pwd)/configs
confPathInContainer=/home/user/daccadevo/configs
priorityParam="-c 128"

if [ ! -d $finalresultsPath ]; then
    mkdir -p $finalresultsPath
fi

inDockerGroup=`id -Gn | grep docker`
if [ -z "$inDockerGroup" ]; then
    sudoCMD="sudo"
else
    sudoCMD=""
fi
dockerCMD="$sudoCMD docker"

if [ -d "$confPath" ]; then
    confVolParam="-v $confPath:$confPathInContainer"
else
    confVolParam=""
fi

exec $dockerCMD run -i --mount type=bind,source=$currentPath,target=$destpath $imageName  "$uid" "$nbRuns" "$configFile"

