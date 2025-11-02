#!/bin/bash
#set -e

uid=$1 #${1:-1000}
nbRuns=$2
configName=$3
shift; shift; shift;

useradd -d /home/user -Ms /bin/bash -u $uid user
chown -R $uid /home/user

echo running as $uid

# Launch illumination
exec bash -c "cd /home/user/daccadevo; python3 -m daccadevo.DACCADRun -c $configName -r $nbRuns"


